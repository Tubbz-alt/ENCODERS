#!/bin/bash

#


# Copyright (c) 2014 SRI International and Suns-tech Incorporated
# Developed under DARPA contract N66001-11-C-4022.
# Authors:
#   Sam Wood (SW)
#   Hasnain Lakhani (HL)

#
# Basic validation that is performed after test execution, to
# confirm that no errors occurred with the execution.
#

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

OUTPUT_FILE=$1
NUM_DEVICES=$2
FAIL_LOG=$3

if [ ! -r "${OUTPUT_FILE}" ]; then
    echo "Could not read output file." >> "${FAIL_LOG}"
    exit 1
fi


NUM_IF=$(grep "usb0" "${OUTPUT_FILE}" | wc -l)

if [ "${NUM_IF}" != "$NUM_DEVICES" ]; then
    echo "Did not read enough ifconfig output: ${NUM_IF} != $NUM_DEVICES" >> "${FAIL_LOG}"
    exit 1
fi

# check for proper shutdown event to catch possible deadlocks
#NUM_SHUTDOWN=$(grep "* SHUTDOWN COMPLETED *" ${OUTPUT_FILE} | wc -l)
#if [ "${NUM_SHUTDOWN}" != "%%num_nodes%%" ]; then
#    echo "Adding delay for haggle to shutdown and to generate core files for processes still running ..." >> ${FAILLOG}
#    sleep 180
#fi

if [ -r "${FAIL_LOG}" ]; then
    NUM_ERRORS=$(wc -l ${FAIL_LOG} | awk '{print $1;}')
    if [ ${NUM_ERRORS} -ne "0" ]; then
        exit 1
    fi
fi

if [ -x "${DIR}/custom_validate.sh" ]; then
    bash "${DIR}/custom_validate.sh" "${OUTPUT_FILE}" "${FAIL_LOG}"
    if [ "$?" != "0" ]; then
        exit 1
    fi
fi

exit 0
