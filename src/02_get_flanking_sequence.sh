#!/bin/bash#!/bin/bash

# Parameters
REFERENCE="genome.fa"
FLANK_SIZE=50

# Index the reference genome if not already indexed
samtools faidx $REFERENCE

# Process each position
while read -r line; do
    CHR=$(echo $line | awk '{print $1}')
    POS=$(echo $line | awk '{print $2}')
    START=$((POS - FLANK_SIZE))
    END=$((POS + FLANK_SIZE))

    # Ensure start is not less than 1
    if [ $START -lt 1 ]; then
        START=1
    fi

    # Extract the sequence
    samtools faidx $REFERENCE "${CHR}:${START}-${END}" >> output/flanking_sequence.fasta
done < positions.txt
