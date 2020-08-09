#!/bin/bash
ls -d tests/*/ | cut -f2 -d'/' >> tests_list
echo "==========" >> summary
while IFS= read -r line
do
    echo "${line}" >> summary
    /usr/bin/time -v -o tests/$line/stats cat tests/$line/input | python3 main.py > tests/$line/out 2> tests/$line/err
    diff -wB tests/$line/expect tests/$line/out >> summary
    #echo "=====" >> summary
    cat tests/$line/err >> summary
    #echo "=====" >> summary
    cat tests/$line/stats | grep "User time" >> summary
    cat tests/$line/stats | grep "System time" >> summary
    cat tests/$line/stats | grep "Maximum resident" >> summary
    echo "==========" >> summary
done < tests_list
cat summary
