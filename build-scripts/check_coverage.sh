#!/bin/sh

echo "\nChecking coverage for Python code\n"

export PYTHONPATH=$PYTHONPATH:tests/functional/;

OUT=`pytest --cov=pylint_mongoengine`;

coverage=`echo "$OUT" | grep TOTAL | sed 's/TOTAL\s*\w*\s*\w*\s*\w*\s*\w\s*//g' | cut -d'%' -f1`;

ERROR=`echo "$OUT" | egrep 'Failed|FAILURE'`

echo 'coverage was:' $coverage'%'
threshold=100
if [ "$ERROR" != "" ]
then
    if [ $coverage -eq $threshold ]
    then
	echo "But something went wrong";
	echo "$OUT";
	exit 1
    else
	echo "And something went wrong"
	echo "$OUT";
	coverage report -m
	exit 1
    fi
fi

if [ $coverage -eq $threshold ]
then
    echo "Yay! Everything ok!";
    exit 0;
else
    coverage report -m
    exit 1
fi
