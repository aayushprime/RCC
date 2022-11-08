#!/usr/bin/bash
#SBATCH --account=pwsu0493
#SBATCH -N 1
#SBATCH --cpus-per-task=1
#SBATCH --job-name=results2
#SBATCH --output=results2_%A.txt
#SBATCH --time=15:00

# sed strings to replace
# 2 : my attempt number
# MyUniqueFolder my working directory
# 0 : weight type
# initialGuess.pickle : initial guess pickle
# 400 : first seed value
# 3 : number of tries


# Assume you have the distance.pickle file in your home directory
# and you copied a bestGuess.pickle file inside your working directory

# make a working directory
cd

mkdir -p MyUniqueFolder

cd MyUniqueFolder

weightType="0"
initialPickle="initialGuess.pickle"
RandSeed="400"
NOfTrys="3"

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
    srun singularity exec -B ~nehrbajo/proj03data ~nehrbajo/python3.sif python3  ~w006jwn/proj03data/tspMod.py $weightType $initialPickle $(($RandSeed+$task)) $NOfTrys >>BEST &
    sleep 1

done
wait