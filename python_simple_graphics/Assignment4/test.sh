#!/bin/bash
./CG_hw4 -f bound-lo-sphere.smf -j 0 -k 0 -o 500 -p 500 -x 0.0 -y 0.0 -z 1.0 -X 0.0 -Y 0.0 -Z 0.0 -q 0.0 -r 0.0 -w -1.0 -Q 0.0 -R 1.0 -W 0.0 -u -0.7 -v -0.7 -U 0.7 -V 0.7 > out.ps
 okular out.ps

./CG_hw4 -f bound-lo-sphere.smf -x -1.0 -z 0.5 -q 1.0 -w -0.5 > out.ps
okular out.ps

./CG_hw4 -f bound-lo-sphere.smf -q 1.0 -w -1.0 > out.ps
okular out.ps


./CG_hw4 -f bound-lo-sphere.smf -x -4.0 -z 5.0 -q 1.0 -w -0.5 > out.ps
okular out.ps

./CG_hw4 -f bound-lo-sphere.smf -k 125 -p 375 -q 1.0 -u -1.4 -U 1.4 > out.ps
okular out.ps

./CG_hw4 -f bound-bunny_200.smf -j 100 -k 50 -o 400 -p 450 -x 0.5 -y 0.2 -z 1.0 -X 0.2 -Y -0.2 -Z 0.3 -q -3.0 -r -2.0 -w 1.0 -Q 3.0 -R -2 -W -4.0 -u -.5 -v -.9 -U 1.2 -V .8 -P > out.ps
okular out.ps

./CG_hw4 -f bound-bunny_200.smf -j 100 -k 50 -o 400 -p 450 -x 0.5 -y 0.2 -z 1.0 -X 0.2 -Y -0.2 -Z 0.3 -q -3.0 -r -2.0 -w 1.0 -Q 3.0 -R -2 -W -4.0 -u -.5 -v -.9 -U 1.2 -V .8 > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf -P > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf -j 0 -k 30 -o 275 -p 305 -P > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf -x 1.5 > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf -x 4.75 -y -3.25 -z 3.3 -P > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf -X 0.25 -Y -0.15 -Z 0.3 > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf -X 0.35 -Y -0.3 -Z 0.3 -u -0.35 -v -0.35 -P > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf -X 0.25 -Y -0.15 -Z 0.3 -j 103 -k 143 -o 421 -p 379 > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf -X 0.35 -Y -0.3 -Z 0.3 -u -0.35 -v -0.35 -j 43 -k 71 -o 201 -p 402 -P > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf -q -1 -r 1.5 -w -2.0 > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf -Q 1.5 -R 1 -W .4 > out.ps
okular out.ps

./CG_hw4 -f bound-cow.smf -u -1.5 -v -0.9 -U 1.2 -V 0.7 > out.ps
okular out.ps

./CG_hw4 -f cube.smf -u -1.5 -v -1.5 -U 1.5 -V 1.5 -F 1 -B -5 > out.ps
okular out.ps

./CG_hw4 -f cube.smf -q 1.5 -r 2 -w 5 -u -1 -v -1 -U 1 -V 1 -z 6 -F 1 -B -5 > out.ps
okular out.ps

./CG_hw4 -f cube.smf -x -4.0 -z 5.0 -q 1.0 -w -0.5 -u -1.0 -v -1.0 -U 1.0 -V 1.0 -F 1 -B -5 > out.ps
okular out.ps

./CG_hw4 -f cube.smf -u -1.5 -v -1.5 -U 1.5 -V 1.5 -F 1 -B -5 -P > out.ps
okular out.ps

./CG_hw4 -f cube.smf -q 1.5 -r 2 -w 5 -u -1 -v -1 -U 1 -V 1 -z 6 -F 1 -B -5 -P > out.ps
okular out.ps

./CG_hw4 -f cube.smf -x -4.0 -z 5.0 -q 1.0 -w -0.5 -u -1.0 -v -1.0 -U 1.0 -V 1.0 -F 1 -B -5 -P > out.ps
okular out.ps
