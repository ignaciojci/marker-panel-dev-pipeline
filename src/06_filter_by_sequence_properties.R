#!/bin/bash

library(dplyr)

# Run samtools idxstats and capture output
system("samtools idxstats sorted.bam", intern = TRUE) %>%
  read.table(text = ., header = FALSE, stringsAsFactors = FALSE) %>%
  rename(Sequence = V1, Length = V2, Hits = V3) %>%
  mutate(Hits = as.numeric(Hits)) %>%
  print()
