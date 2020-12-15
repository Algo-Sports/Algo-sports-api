#!/bin/bash
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
    -s | --source)
        SOURCE_FILE="$2"
        shift
        shift
        ;;
    -r | --run-cmd)
        RUN_CMD="$2"
        shift
        shift
        ;;
    -c | --compile-cmd)
        COMPILE_CMD="$2"
        shift
        shift
        ;;
    -p1 | --parameter1)
        PARAMETER1="$2"
        shift
        shift
        ;;
    -p2 | --parameter2)
        PARAMETER2="$2"
        shift
        shift
        ;;
    *)
        echo "Unknown option $key"
        echo "Usage: ./run [--language <language>] [--isolate]"
        exit -1
        ;;
    esac
done

if [[ $COMPILE_CMD != "" ]]; then
    bash -c "$COMPILE_CMD $SOURCE_FILE"
    bash -c "$RUN_CMD $SOURCE_FILE"
else
    bash -c "$RUN_CMD $SOURCE_FILE $PARAMETER1 $PARAMETER2"
fi
