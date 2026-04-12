#!/bin/bash

# Clean up old files
rm -f mclj_in.dat mclj_out.dat log.dat

# Compile programs
echo "Compiling..."
gcc -o lmclj ../lmclj.c ../getval.c -lm
gcc -o mclj ../mclj.c ../getval.c -lm
gcc -o zmclj ../zmclj.c ../getval.c -lm
gcc -o amclj ../amclj.c ../getval.c -lm

# Parameters in reduced units (Argon triple point)
N=256
RHO=0.8445
TEMP=0.6995
DISP=0.1
DR=0.02
NTSKIP=10
NTPRINT=100
NTJOB=5000

echo "Generating initial configuration..."
printf "${N}\n${RHO}\n${TEMP}\n${DISP}\n${DR}\n${NTSKIP}\n${NTPRINT}\n${NTJOB}\nmclj_in.dat\n" | ./lmclj


# -------------------------
#  Equilibration run
# -------------------------
./mclj

# -------------------------
#  Reset averages
# -------------------------
printf "mclj_out.dat\n${N}\n${RHO}\n${TEMP}\n${DISP}\n${DR}\n10\n100\n50000\nmclj_in.dat\n" | ./zmclj


echo "Running simulation..."
./mclj | tee log.dat

echo "Analyzing results..."
echo "y" | ../amclj | tee amclj.logprintf "mclj_out.dat\ny\n" | ../amclj | tee amclj.log

echo "Done! Results in log.dat and amclj.log"