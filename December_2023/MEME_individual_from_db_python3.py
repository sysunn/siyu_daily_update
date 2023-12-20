#! /usr/bin/python
import sys
import re

def separate_motifs(filename):
    with open(filename, 'r') as infile:
        current_motif_lines = []
        current_motif_name = None
        meme_version = ''
        alphabet = ''
        strands = ''
        motif_letter_freq = ''
        background_letter_freq = ''
        weight_matrix = ''
        in_weight_matrix = False
        
        while True:
            line = infile.readline()
            if not line:
                break
            line = line.strip()
            
            if line.startswith('MEME version'):
                meme_version = line
            elif line.startswith('ALPHABET'):
                alphabet = line
            elif line.startswith('strands:'):
                strands = line
            elif line.startswith('Background letter frequencies'):
                background_letter_freq = line
                next_line = infile.readline().strip()
                while next_line:
                    background_letter_freq += '\n' + next_line
                    next_line = infile.readline().strip()
            elif line.startswith('letter-probability matrix'):
                weight_matrix = line
                in_weight_matrix = True
                next_line = infile.readline().strip()
                while next_line:
                    weight_matrix += '\n' + next_line
                    next_line = infile.readline().strip()
            elif line.startswith('Stopped because maximum number of motifs'):
                in_weight_matrix = False
            
            if line.startswith('MOTIF'):
                if current_motif_name:
                    write_motif_to_file(current_motif_name, current_motif_lines, meme_version, alphabet, strands, background_letter_freq, weight_matrix)
                current_motif_name = line.split()[1]
                current_motif_lines = [line]
                in_weight_matrix = False
            elif not in_weight_matrix:
                current_motif_lines.append(line)
        
        # Write the last motif
        if current_motif_name:
            write_motif_to_file(current_motif_name, current_motif_lines, meme_version, alphabet, strands, background_letter_freq, weight_matrix)

def write_motif_to_file(motif_name, motif_lines, meme_version, alphabet, strands, background_letter_freq, weight_matrix):
    with open(motif_name + '_output.txt', 'w') as outfile:
        outfile.write(meme_version + '\n\n')
        outfile.write(alphabet + '\n\n')
        outfile.write(strands + '\n\n')
        outfile.write(background_letter_freq + '\n\n')

        for line in motif_lines:
            outfile.write(line + '\n')

        outfile.write('\n\n')
        outfile.write(weight_matrix + '\n')

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py input_filename")
        sys.exit(1)
    input_filename = sys.argv[1]
    separate_motifs(input_filename)

if __name__ == "__main__":
    main()
