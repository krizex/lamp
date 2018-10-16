#!/bin/bash

while read line
do
    if [[ $line == \#* ]]; then
        continue
    fi

    if [[ $line == "" ]]; then
        continue
    fi

    IFS=' ' read -r -a array <<< "$line"
    #sqlite3 test.db "select * from abc;" ".exit"
    sqlite3 database.db "insert into candidate values (\"${array[0]}\", ${array[1]}, ${array[2]}, ${array[3]}, ${array[4]}, \"\")"
    sqlite3 database.db "update candidate set start_pe=${array[1]}, stop_pe=${array[2]}, start_price=${array[3]}, own=${array[4]} where code=\"${array[0]}\""
done < source.txt
