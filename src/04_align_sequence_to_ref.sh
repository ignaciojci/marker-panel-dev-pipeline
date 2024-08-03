#!/bin/bash

indir=output
sample=flanking_sequence.fasta

bowtie2 -x ${ref%.fasta} -U "$indir/${sample}.fastq" -S "${outdir}/${sample}.sam"