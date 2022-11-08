#!/usr/bin/bash
# Name: Soham Roy
# wNumber: w218sxr
# Project name: proj03
# Assigned: Oct 20
# Due date: Nov 04
# Tested on: fry

fry=w218sxr@fry.cs.wright.edu
owens=w218sxr@owens.osc.edu
aws=ubuntu@3.234.5.187


# $1 = weightType, $2 = initialGuess.pickle, $3 = RandSeed, $4 = #OfTrys, $5 = #OfBatchJobs


# Use only "ssh scp sed cut ls pwd cd chmod at sbatch scancel squeue -u echo grep "

if [ -f ./TERMINATE ]; then
    echo "The program did not start. Please remove the TERMINATE file before starting the program."
    exit 0
fi


touch STARTED

begin="1"
end="$5"


initialGuessPickle=$2;
if [ -f ./savedState.txt ]; then
    echo "savedState.txt was fond. The program will continue from where it left off."
    begin=$(head -n 1 savedState.txt)
    initialGuessPickle="savedPickle.pickle";
fi


# uniqueFolder=$(mktemp -d -u -t 'XXXXX' | cut -d '/' -f 3)
uniqueFolder="MyUniqueFolder"
weightType=$1

for task in $(seq $begin $end);
do
    echo Inside For
    # Launch tasks 
    # fry
    cp fryTemplate.sbatch fry.sbatch;
    sed -i "s/MYDIR/$uniqueFolder/g" fry.sbatch;
    sed -i "s/MYATTEMPT/$task/g" fry.sbatch;
    sed -i "s/WEIGHT_TYPE/$1/g" fry.sbatch;
    sed -i "s/INITIAL_GUESS_PICKLE/$initialGuessPickle/g" fry.sbatch;
    sed -i "s/RANDSEED/$3/g" fry.sbatch;
    sed -i "s/NOFTRYS/$4/g" fry.sbatch;

    # copy required files to remote machine
     scp tspMod.py $fry:~
     scp distance0$1.pickle $fry:~
     scp $initialGuessPickle $fry:~

    # launch task on remote machine
     scp fry.sbatch $fry:~
    fry_job=$( ssh $fry "sbatch fry.sbatch")
    fry_job_id=$(echo $fry_job | cut -d " " -f 4)


    echo Launched on fry

    # owens
    cp owensTemplate.sbatch owens.sbatch;
    sed -i "s/MYDIR/$uniqueFolder/g" owens.sbatch;
    sed -i "s/MYATTEMPT/$task/g" owens.sbatch;
    sed -i "s/WEIGHT_TYPE/$1/g" owens.sbatch;
    sed -i "s/INITIAL_GUESS_PICKLE/$initialGuessPickle/g" owens.sbatch;
    sed -i "s/RANDSEED/$3/g" owens.sbatch;
    sed -i "s/NOFTRYS/$4/g" owens.sbatch;

    # copy required files to remote machine
     scp tspMod.py $owens:~
     scp distance0$1.pickle $owens:~
     scp $initialGuessPickle $owens:~

    # launch task on remote machine
     scp owens.sbatch $owens:~
    owens_job=$( ssh $owens "sbatch owens.sbatch")
    owens_job_id=$(echo $owens_job | cut -d " " -f 4)
    
    echo Launched on owens


    # AWS launch command
    # echo "ssh $aws \"srun singularity exec ~w006jwn/python3.sif python3 tspMod.py $1 $initialPickle $(($3+32)) $4 > BESTAWS &\"" | at now;
    cp awsTemplate.sh aws.sh;
    sed -i "s/WEIGHT_TYPE/$weightType/g" aws.sh;
    sed -i "s/INITIAL_GUESS_PICKLE/$initialGuessPickle/g" aws.sh;
    sed -i "s/RANDSEED/$3/g" aws.sh;
    sed -i "s/NOFTRYS/$4/g" aws.sh;
    sed -i "s/OWENSADDR/$owens/g" aws.sh;

    scp  $initialGuessPickle $aws:~/proj03data/
    scp  ./aws.sh $aws:~
    ssh  $aws "chmod +x aws.sh"
    ssh  $aws screen -d -m "nohup ~/aws.sh & disown"

    echo Launched on aws
    echo $owens_job $fry_job

    # WAITING FOR JOBS TO FINISH

    # *) Look for all 3 systems finished before proceeding
    #     to the next #OfBatchJobs itteration loop
    # wait for all 3 systems to finish  
    
    active=$( ssh $fry "squeue -u \$USER | grep $fry_job_id")
    while [ -n "$active" ]
    do 
        sleep 1
        active=$( ssh $fry "squeue -u \$USER | grep $fry_job_id")
    done
     scp $fry:~/$uniqueFolder/BEST ./bestFry

    echo "READ from fry (fry job complete)"
    echo $(cat bestFry)


    active=$( ssh $owens "squeue -u \$USER | grep $owens_job_id")
    while [ -n "$active" ]
    do 
        sleep 1
        active=$( ssh $owens "squeue -u \$USER | grep $owens_job_id")
    done
     scp $owens:~/$uniqueFolder/BEST ./bestOwens

    echo "READ from owens (owens job complete)"
    echo $(cat bestOwens)

    # Still to do for aws
    # wait for aws to complete
    until scp  $aws:~/proj03data/FINISHED ./bestAWS; do
        sleep 1
    done
    scp  $aws:~/proj03data/BEST ./bestAWS
    echo "READ from aws (aws job complete)"
    echo $(cat bestAWS)


    # Find the best of the 3 systems
    bestFry=$(cat bestFry | sort -k2 -n | head -n 1);
    bestOwens=$(cat bestOwens | sort -k2 -n | head -n 1);
    bestAws=$(cat bestAWS);

    bestFryCost=$(echo $bestFry | cut -d" " -f2);
    bestOwensCost=$(echo $bestOwens | cut -d" " -f2);
    bestAwsCost=$(echo $bestAws | cut -d" " -f2);

    bestFrySeed=$(echo $bestFry | cut -d":" -f1 | cut -d"_" -f2);
    bestOwensSeed=$(echo $bestOwens | cut -d":" -f1 | cut -d"_" -f2);
    bestAwsSeed=$(echo $bestAws | cut -d":" -f1 | cut -d"_" -f2);
    echo "bestFrySeed: $bestFrySeed"
    echo "bestOwensSeed: $bestOwensSeed"
    echo "bestAwsSeed: $bestAwsSeed"

    echo "bestFryCost: $bestFryCost"
    echo "bestOwensCost: $bestOwensCost"
    echo "bestAwsCost: $bestAwsCost"


    # Pull data from all 3 systems
    # save as "bestIFoundSoFar.pickle"
    if [[ $bestFryCost -lt $bestOwensCost && $bestFryCost -lt $bestAwsCost ]]; then
         scp $fry:~/$uniqueFolder/best_$bestFrySeed.pickle ./bestIFoundSoFar0$weightType.pickle
        bestIFoundSoFar=$bestFryCost
    elif [[ $bestOwensCost -lt $bestFryCost && $bestOwensCost -lt $bestAwsCost ]]; then
         scp $owens:~/$uniqueFolder/best_$bestOwensSeed.pickle ./bestIFoundSoFar0$weightType.pickle
        bestIFoundSoFar=$bestOwensCost
    else
        scp  $aws:~/proj03data/best_$bestAwsSeed.pickle ./bestIFoundSoFar0$weightType.pickle
        bestIFoundSoFar=$bestAwsCost
    fi

    echo "bestIFoundSoFar: $bestIFoundSoFar"

    # Pull from OSC using update03.sh and grab current best. If
    # you beat the best, submit to update03.sh on OSC
    bestDistOSC=$( ssh $owens "./proj03data/update03.sh $1")
    echo bestDistOSC = $bestDistOSC
    if [ "$bestDistOSC" -gt "$bestIFoundSoFar" ]; then
        echo "Submitting the best I found so far to owens server"
         scp bestIFoundSoFar0$weightType.pickle $owens:~/$uniqueFolder/
         ssh $owens "python3 -c \"import pickle;f=open('./$uniqueFolder/bestIFoundSoFar0$weightType.pickle','rb');print(pickle.load(f));print(pickle.load(f))\" > bestIFoundSoFar0$weightType.txt"        
         ssh $owens "./proj03data/update03.sh $1 ./bestIFoundSoFar0$weightType.txt"
    fi


     # *) All 3 systems will use the same initialGuess.pickle at the
    #     start of each new job. However your initialGuess.pickle
    #     should be updated to the last bestIFoundSoFar.pickle
    #     file or the current best from the update03.sh data base
    #     afer running a complete itteration of the #OfBatchJobs
    #     itteration.
    cp bestIFoundSoFar0$weightType.pickle initialGuess.pickle;


    # *) While looking for all 3 systems to be finished, if your
    #     workflow.sh script sees TERMINATE, then save its state as
    #     savedState.pickle and end your script.
    if [ -f ./TERMINATE ]; then
        # save state as savedState.pickle
        echo Terminate found!
        echo $task > ./savedState.txt
        cp bestIFoundSoFar0$weightType.pickle savedState.pickle
        break;
    fi
   
done;

touch FINISHED