#!/bin/bash

while read line
do
    if [[ $line == \#* ]]; then
        continue
    fi
    IFS=' ' read -r -a array <<< "$line"
    #sqlite3 test.db "select * from abc;" ".exit"
    sqlite3 database.db "insert into candidates values (\"${array[0]}\", ${array[1]}, ${array[2]}, ${array[3]}, ${array[4]}, \"\")"
done < source.txt
