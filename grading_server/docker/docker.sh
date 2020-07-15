#!/bin/bash
lang=$1
if [[ $lang == "py" ]]
then
    #file_name_hash=$(echo -n $2 | md5sum | awk '{print $1}')
    $file_name_hash=$4
    docker build -f ./docker/Dockerfile-py -t $file_name_hash --build-arg FILE=$2 --build-arg TEST_FOLDER=$3 .
    docker run --rm --memory=100000k $file_name_hash
else
    echo "unknown language $lang"
fi