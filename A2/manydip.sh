#!/usr/bin/env bash

DISPS=(0.05 0.10 0.15 0.20 0.25)

N=256
RHO=0.8445
TEMP=0.6995
DR=0.02
NTSKIP=10
NTPRINT=100
NTJOB=5000

echo "Compiling..."
gcc -o lmclj ../lmclj.c ../getval.c -lm
gcc -o mclj  ../mclj.c  ../getval.c -lm
gcc -o zmclj ../zmclj.c ../getval.c -lm

for DISP in "${DISPS[@]}"
do
    echo "====================================="
    echo "Running for DISP = $DISP"
    echo "====================================="

    rm -f mclj_in.dat mclj_out.dat log.dat

    printf "%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n" \
      "$N" "$RHO" "$TEMP" "$DISP" "$DR" "$NTSKIP" "$NTPRINT" "$NTJOB" "mclj_in.dat" \
      | ./lmclj

    ./mclj > /dev/null

    printf "%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n" \
      "mclj_out.dat" "$N" "$RHO" "$TEMP" "$DISP" "$DR" "$NTSKIP" "$NTPRINT" "$NTJOB" "mclj_in.dat" \
      | ./zmclj

    ./mclj > log.dat
    cp log.dat "log_disp_${DISP}.dat"
done

echo "All short simulations completed."