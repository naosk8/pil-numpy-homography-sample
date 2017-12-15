#!/bin/sh
cd `dirname $0`
echo python ./main.py -i ./img/sample.png -c "78, 114, 18, 258, 390, 230, 342, 18"
python ./main.py -i ./img/sample.png -c "78, 114, 18, 258, 390, 230, 342, 18"
