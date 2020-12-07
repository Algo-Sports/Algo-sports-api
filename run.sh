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
    *)
        echo "Unknown option $key"
        echo "Usage: ./run [--language <language>] [--isolate]"
        exit -1
        ;;
    esac
done

if [[ $COMPILE_CMD != "" ]]; then
    bash -c "$COMPILE_CMD"
    bash -c "$RUN_CMD"
else
    echo "" | bash -c "$RUN_CMD $SOURCE_FILE"
fi
