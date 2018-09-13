#!/bin/sh

echo "\nChecking coverage for Python code\n"

coverage=`pytest --cov=$1 | grep TOTAL | sed 's/TOTAL\s*\w*\s*\w*\s*\w*\s*\w\s*//g' | cut -d'%' -f1`;
ERROR=$?

echo 'coverage was:' $coverage'%'

if [ "$ERROR" != "0" ]
then
    if [ $coverage -eq $2 ]
    then
	echo "But something went wrong";
	coverage report -m
	exit 1
    else
	echo "And something went wrong"
	coverage report -m
	exit 1
    fi
fi

if [ $coverage -eq $2 ]
then
    echo "Yay! Everything ok!";
    exit 0;
else
    coverage report -m
    exit 1
fi
