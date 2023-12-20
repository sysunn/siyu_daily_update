#! /usr/bin/python
import sys

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
        outfile.write(meme_version + '\n\n')
        outfile.write('\n')  # Empty line
        outfile.write(alphabet + '\n\n')
        outfile.write('\n')  # Empty line
        outfile.write(strands + '\n\n')
        outfile.write('\n')  # Empty line
        outfile.write(motif_letter_freq + '\n\n')
        outfile.write('\n')  # Empty line
        outfile.write(background_letter_freq + '\n\n')
        outfile.write('\n')  # Empty line
        
        for line in motif_lines:
            outfile.write(line + '\n')

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py input_filename")
        sys.exit(1)
    input_filename = sys.argv[1]
    separate_motifs(input_filename)

if __name__ == "__main__":
    main()
