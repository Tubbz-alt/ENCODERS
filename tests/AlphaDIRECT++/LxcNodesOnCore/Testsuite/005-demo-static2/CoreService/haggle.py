#
# CORE
# Copyright (c)2010-2012 the Boeing Company.
# See the LICENSE file included in this distribution.
#
# Suns-tech work product.
#
''' demo-static1
'''

import os
import tempfile
from utils import *

from core.service import CoreService, addservice
from core.misc.ipaddr import IPv4Prefix, IPv6Prefix

USER=get_username()
TESTAPP=get_app_name()
OUTPUTFILE=get_tmp_name()
CFGFILE=get_cfg_name()

class HaggleService(CoreService):
    ''' This is a sample user-defined service. 
    '''
    # a unique name is required, without spaces
    _name = "HaggleService"
    # you can create your own group here
    _group = "Utility"
    # list of other services this service depends on
    _depends = ()
    # per-node directories
    _dirs = ("/home/%s/.Haggle/" % (USER,) ,)
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    _configs = ('haggleservice.sh', )
    # this controls the starting order vs other enabled services
    _startindex = 50
    # list of startup commands, also may be generated during startup
    _startup = ('sh haggleservice.sh', )
    # list of shutdown commands
    _shutdown = ()

    @classmethod
    def generateconfig(cls, node, filename, services):
        ''' Return a string that will be written to filename, or sent to the
            GUI for user customization.
        '''
        cfg = "#!/bin/sh\n"
        cfg += "# this file, haggleservice.sh, auto-generated by HaggleService (haggle.py)\n"
        for ifc in node.netifs():
            cfg += 'echo "Node %s has interface %s"\n' % (node.name, ifc.name)
            # here we do something interesting 
            cfg += "\n".join(map(cls.subnetentry, ifc.addrlist))
            break
        cfg += "/sbin/ifconfig eth0 broadcast 10.0.0.255\n"
        cfg += "/sbin/route add default eth0\n"
        cfg += "cp %s ~/.Haggle/config.xml\n" % (CFGFILE,) 
        cfg += "/bin/su - %s -c \"/usr/local/bin/haggle -dd -f &\"\n" % (USER,)
        cfg += "/bin/su - %s -c \"%s %s %s &\"\n" % (USER, TESTAPP, node.name, OUTPUTFILE)
        cfg += "/bin/su - %s -c \"sleep 20 && kill -INT $(cat ~/.Haggle/haggle.pid)\"\n" % (USER,)
        # make sure haggle is killed for good
        cfg += "/bin/su - %s -c \"sleep 2 && kill $(cat ~/.Haggle/haggle.pid)\"\n" % (USER,)
        return cfg

    @staticmethod
    def subnetentry(x):
        ''' Generate a subnet declaration block given an IPv4 prefix string
            for inclusion in the config file.
        '''
        if x.find(":") >= 0:
            # this is an IPv6 address
            return ""
        else:
            net = IPv4Prefix(x)
            return 'echo "  network %s"' % (net)

# this line is required to add the above class to the list of available services
addservice(HaggleService)

