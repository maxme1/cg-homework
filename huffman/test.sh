#!/usr/bin/env bash

python encode.py $1 $2
python decode.py $2 $3
echo Input size
ls -lh $1
echo Encoded size
ls -lh $2
echo Contents diff
diff $1 $3
