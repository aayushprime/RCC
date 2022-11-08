#!/usr/bin/bash
weightType="0"
initialPickle="initialGuess.pickle"
Seed="400"
NOfTrys="3"
owens="w218sxr@owens.osc.edu"



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
