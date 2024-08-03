#!/bin/bash

samtools view -bS input.sam > input.bam

samtools sort input.bam -o sorted.bam
samtools index sorted.bam

samtools idxstats sorted.bam
