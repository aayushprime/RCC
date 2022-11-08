#!/usr/bin/bash
weightType="WEIGHT_TYPE"
initialPickle="INITIAL_GUESS_PICKLE"
Seed="RANDSEED"
NOfTrys="NOFTRYS"
owens="OWENSADDR"



touch STARTED
if [ -f ./FINISHED ]; then
    rm FINISHED
fi

# python3 tspMod.py $weightType $initialPickle $((32+$Seed)) $NOfTrys >BEST

scp -r $owens:~/proj03data/ .
scp $owens:~/python3.sif ~/python3.sif

cd ~/proj03data
singularity exec ~/python3.sif python3 tspMod.py $weightType $initialPickle $((32+$Seed)) $NOfTrys >BEST

touch FINISHED
rm STARTED
