#!/usr/bin/bash
#
# Exit codes
#  0 normal
#  1 usage
#  2 File DNE
#  3 not valid weightType
#  4 weightType not ready yet
#  5 wrong number of inputs 0 or 1 or 2
#  6 wrong number of lines in inFile
#  7 Dos format
#  8 wrong 1st line in inFile or not an integer
#  9 wrong 2nd line in inFile
# 10 wrong distance calculated - must be integer

function usage {
    # inputs: none
    echo "syntax:"
    echo "update03.sh            Prints this usage message"
    echo "update03.sh -1         Prints integer -  max distanceXX.pickle file available"
    echo "update03.sh 0-9        Prints best distance for weight type"
    echo "update03.sh 0-9 inFile Used to submit next best distance"
    echo
    echo "# Outputs possibilitie - submitting next best distance:"
    echo
    echo "GIGO                   Garbage In, Garbage Out."
    echo "SORRY                  Not the best solution"
    echo "BEST                   Your solution was the best solution"
    exit 1
}

function help {
    #inputs: none
    usage
}

function fileDNE {
    # inputs: $1   filename
    echo "The file $1 DNE"
    echo "Please enter a valid file"
    exit 2
}

function nonInteger {
    # inputs: $1   weightType
    echo "The weightType entered is not a valid integer"
    echo "You entered $1"
    echo "Please try again"
    exit 3
}

function typeNotReady {
    # inputs: $1   weightType
    echo "The weightType you entered is not ready yet"
    echo "You entered $1"
    echo "Please try again"
    exit 4
}

function numInputsBad {
    #inputs: $@
    echo "You entered more than 2 inputs and they were"
    echo $@
    echo "Please try again"
    exit 5
}


# ********************************************************************************
# Main code starts here
maxWeight=2

# no args
if [ "$#" -lt 1 ]; then
    usage
fi

# too many args
if [ "$#" -gt 2 ]; then
    numInputsBad
fi

# Check for  keywords (help, -help, --help)
if [ "$1" == "help" ] || [ "$1" == "-help" ] || [ "$1" == "--help" ]; then
    usage
fi

# Check if the index is -1
if [ "$1" == "-1" ]; then
    echo "$maxWeight"
    exit 0
fi

# Check if the index is valid
if ! [[ "$1" =~ ^[0-9]+$ ]]; then
    #    The ! negates the logic
    #    The ^ indicates the beginning of the input pattern
    #    [0-9] is a range of characters from zero to nine
    #    The + means "1 or more of the preceding ([0-9])"
    #    The $ indicates the end of the input pattern
    nonInteger $1
fi

# Check if weightType > maxWeight
if [ "$1" -gt "$maxWeight" ]; then
    typeNotReady $1
fi

# get the best distance so far
database=./database0${1}.txt
bestDist=`cat $database |tail -n 5 | head -n 1`

# Check if only 1 arg passed
# ( print bestDist)
if [ "$#" -lt 2 ]; then
    echo $bestDist
    exit 0
fi
	
# Check if the file exists
if [ ! -f "$2" ]; then
    fileDNE $2
fi

# Validate the inFile
#     6 wrong number of lines in inFile
numLines=`wc -l "$2"|cut -d" " -f1`
if ! [ "$numLines" == 2 ]; then
    echo "GIGO"
    echo "numlines error"
    exit 6
fi

dosfile=`file $2 | grep CRLF | wc -c`
if [ "$dosfile" -gt 0 ]; then
    echo "GIGO"
    echo "dosfile error"
    exit 7
fi

myDist=`head -n 1 $2`
numWords=`echo $myDist | wc -w`
if [ "$numWords" -gt 1 ]; then
    echo "GIGO"
    echo "numwords"
    exit 8
fi

# Check if the myDist is a valid integer
if ! [[ "$1" =~ ^[0-9]+$ ]]; then
    echo "GIGO"
    echo "mydist invalid"
    exit 8

fi

mylist=`tail -n 1 $2`
# Check only 1 left, 1 right bracket and 483 commas
# Check only 1 left, 1 right bracket and 823 commas
left=`echo "${mylist:0:1}"`
right=`echo "${mylist: -1}"`
comma=`echo "$mylist" |grep -o ',' | wc -l`

if [ "$left" != '[' ] ||  [ "$right" != ']' ] || [ "$comma" != "822" ]; then
    echo "GIGO"
    echo $left:$right:$comma
    echo "left right stuff"
    exit 9
fi

#echo $mylist

singList=${mylist//[}
#echo one:$singList
singList=${singList//]}
#echo two:$singList
singList=${singList//,/" "}
#echo three:$singList
#echo "done"
# check only 484 ints
# check only 823 ints
numInts=`echo "$singList" | xargs -n1 | sort -u | wc -l | cut -d " " -f1`
if [ "$numInts" != "823" ]; then
    echo "GIGO"
    echo "singList??"
    exit 9
fi

singListArray=($singList)
for i in "${singListArray[@]}"; do
    # Check for valid integers
    if ! [[ "$i" =~ ^[0-9]+$ ]]; then
	echo "GIGO"
    echo "invalid ints??"
	exit 9
    fi
done

calcDist=`singularity exec ~nehrbajo/python3.sif python3 ~nehrbajo/proj03data/checkDist.py $1 $singList`
if [ "$calcDist" != "$myDist" ]; then
    echo "GIGO"
    echo "calc dist not equal to my dist"
    exit 10
fi

# get the best distance so far again
bestDist=`cat database0${1}.txt |tail -n 5 | head -n 1`
if [ "$myDist" -lt "$bestDist" ]; then
    echo "BEST"
    echo "$myDist" >> $database
    echo "$mylist" >> $database
    wNumber=`grep $USER ~nehrbajo/quiz04/names | cut -d"," -f1`
    echo "$wNumber" >> $database
    echo `date` >> $database
    lineBreak=`printf '%.s_' $(seq 1 40)`
    echo "$lineBreak" >> $database
else
    echo "SORRY"
fi
