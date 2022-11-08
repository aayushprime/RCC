#!/usr/bin/bash
#SBATCH --account=pwsu0493
#SBATCH -N 1
#SBATCH --cpus-per-task=1
#SBATCH --job-name=resultsMYATTEMPT
#SBATCH --output=resultsMYATTEMPT_%A.txt
#SBATCH --time=15:00

# sed strings to replace
# MYATTEMPT : my attempt number
# MYDIR my working directory
# WEIGHT_TYPE : weight type
# INITIAL_GUESS_PICKLE : initial guess pickle
# RANDSEED : first seed value
# NOFTRYS : number of tries


# Assume you have the distance.pickle file in your home directory
# and you copied a bestGuess.pickle file inside your working directory

# make a working directory
cd

mkdir -p MYDIR

cd MYDIR

weightType="WEIGHT_TYPE"
initialPickle="INITIAL_GUESS_PICKLE"
RandSeed="RANDSEED"
NOfTrys="NOFTRYS"

# create a symbolic link to the distance.pickle file in your home directory
# so that you do not need to copy it all the time
ln -s ../distance0$weightType.pickle distance0$weightType.pickle
ln -s ../$initialPickle $initialPickle

# If you keep a copy of tspMod.py in your home directory
# then you only need to upload a new version if changes are made
# You can upload it to your home directory
if [ ! -f tspMod.py ]; then
    echo "tspMod.py not found in your home directory"
    ln -s ../tspMod.py tspMod.py
fi



# run 16 tasks
rm BEST

for task in $(seq 16 31);

do
    srun singularity exec -B ~nehrbajo/proj03data ~nehrbajo/python3.sif python3  ~nehrbajo/proj03data/tspMod.py $weightType $initialPickle $(($RandSeed+$task)) $NOfTrys >>BEST &
    # srun singularity exec ~nehrbajo/python3.sif python3 ./tspMod.py $weightType $initialPickle $(($RandSeed+$task)) $NOfTrys >>BEST &
    sleep 1

done
wait