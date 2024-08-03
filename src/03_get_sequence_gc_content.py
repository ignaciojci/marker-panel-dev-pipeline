#!/bin/bashimport pysam

# Parameters
reference_file = 'genome.fa'
flank_size = 50

# Function to calculate GC content
def calculate_gc_content(sequence):
    gc_count = sum(1 for base in sequence if base in 'GCgc')
    total_count = len(sequence)
    return (gc_count / total_count) * 100

# Open the reference genome
samfile = pysam.FastaFile(reference_file)

# Print the header
print("Marker\tChromosome\tPosition\tLeft_Flank\tRight_Flank\tGC_Content_Left\tGC_Content_Right")

# Read the list of positions
with open('positions.txt') as f:
    for line in f:
        chr_name, pos = line.strip().split()
        pos = int(pos)
        start_left = max(1, pos - flank_size)
        end_left = pos - 1
        start_right = pos + 1
        end_right = pos + flank_size

        # Extract the left and right sequences
        left_sequence = samfile.fetch(chr_name, start_left - 1, end_left)
        right_sequence = samfile.fetch(chr_name, start_right - 1, end_right)
        
        # Calculate GC content
        gc_content_left = calculate_gc_content(left_sequence)
        gc_content_right = calculate_gc_content(right_sequence)
        
        # Print results
        print(f"{chr_name}:{pos}\t{chr_name}\t{pos}\t{left_sequence}\t{right_sequence}\t{gc_content_left:.2f}\t{gc_content_right:.2f}")

# Close the file
samfile.close()
