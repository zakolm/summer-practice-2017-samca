#!/bin/bash
if [ ! -f file_1.txt ]
	then echo Файла file_1.txt не существует; rm file.txt
	else cat file_1.txt > file.txt
fi
python3 main.py
diff -s -q -w f_out.txt out1.txt

if [ ! -f file_2.txt ]
	then echo Файла file_2.txt не существует; rm file.txt
	else cat file_2.txt > file.txt
fi
python3 main.py
diff -s -q -w f_out.txt out2.txt

if [ ! -f file_3.txt ]
	then echo Файла file_3.txt не существует; rm file.txt
	else cat file_1.txt > file.txt
fi
python3 main.py
diff -s -q -w f_out.txt out3.txt

if [ ! -f file_4.txt ]
	then echo Файла file_4.txt не существует; rm file.txt
	else cat file_1.txt > file.txt
fi
python3 main.py
diff -s -q -w f_out.txt out4.txt

if [ ! -f file_5.txt ]
	then echo Файла file_5.txt не существует; rm file.txt
	else cat file_5.txt > file.txt
fi
python3 main.py
diff -s -q -w f_out.txt out5.txt

if [ ! -f file_6.txt ]
	then echo Файла file_6.txt не существует; rm file.txt
	else cat file_6.txt > file.txt
fi
python3 main.py
diff -s -q -w f_out.txt out6.txt