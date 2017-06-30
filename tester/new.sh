#!/bin/bash
for i in {1..6}
do
	if [ ! -f file_$i.txt ]
		then echo Файла file_$i.txt не существует
		else cat file_$i.txt > file.txt
	fi
	python3 main.py
	diff -s -q -w f_out.txt out$i.txt
done
