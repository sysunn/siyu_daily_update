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
            elif line.startswith('Letter frequencies in dataset:'):
                motif_letter_freq = line
                next_line = infile.readline().strip()
                while next_line:
                    motif_letter_freq += '\n' + next_line
                    next_line = infile.readline().strip()
            elif line.startswith('Background letter frequencies'):
                background_letter_freq = line
                next_line = infile.readline().strip()
                while next_line:
                    background_letter_freq += '\n' + next_line
                    next_line = infile.readline().strip()
            
            if line.startswith('MOTIF'):
                if current_motif_name:
                    write_motif_to_file(current_motif_name, current_motif_lines, meme_version, alphabet, strands, motif_letter_freq, background_letter_freq)
                current_motif_name = line.split()[1]
                current_motif_lines = [line]
            else:
                current_motif_lines.append(line)
        
        # Write the last motif
        if current_motif_name:
            write_motif_to_file(current_motif_name, current_motif_lines, meme_version, alphabet, strands, motif_letter_freq, background_letter_freq)

def write_motif_to_file(motif_name, motif_lines, meme_version, alphabet, strands, motif_letter_freq, background_letter_freq):
    with open(motif_name + '_meme.txt', 'w') as outfile:
        outfile.write(meme_version + '\n')
        outfile.write(alphabet + '\n\n')
        outfile.write(strands + '\n\n')
        outfile.write(motif_letter_freq + '\n')
        outfile.write(background_letter_freq + '\n\n')

        # Extract motif-specific information
        motif_content = '\n'.join(motif_lines)
        motif_info = re.search(r'MOTIF\s+{}(.*?)Time'.format(motif_name), motif_content, re.DOTALL)
        if motif_info:
            motif_content = motif_info.group(1)
            outfile.write('MOTIF\t' + motif_name + '\n')
            outfile.write(motif_content.strip())

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py input_filename")
        sys.exit(1)
    input_filename = sys.argv[1]
    separate_motifs(input_filename)

if __name__ == "__main__":
    main()
