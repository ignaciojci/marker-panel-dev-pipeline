#!/bin/bash

# Filter for genotyping quality (GQ), MAF, call rate, HWE

module load vcftools

input=$1

vcftools --vcf $input --get-INFO GQ --out gq_info
vcftools --vcf $input --freq --out maf
vcftools --vcf $input --missing-site --out missing
vcftools --vcf $input --hardy --out hwe
