#!/bin/bash
for((i=0; ;++i)); do
    /bin/bash ./testscript.sh
    #sleep 1
    python -W ignore engine.py
done
