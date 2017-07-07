#!/bin/bash
if [ ! -f file_1.txt ]
	then echo Файла file_1.txt не существует; rm file.txt
	else cat file_1.txt > file.txt
fi
python3 main.py
diff -s -q -w f_out.txt out1.txt
done
