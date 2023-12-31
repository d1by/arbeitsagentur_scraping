#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "please pass  correct arguments"
    exit 1
fi

JOB_ID="$1"
ERROR_FILE="$2"

if [ ! -f "$ERROR_FILE" ]; then
    exit 1
fi

while true
do
    if [ -s "$ERROR_FILE" ]; then
		echo "Error file has data. Cancelling job $JOB_ID"
        scancel $JOB_ID
        break
    fi
    sleep 5
done
