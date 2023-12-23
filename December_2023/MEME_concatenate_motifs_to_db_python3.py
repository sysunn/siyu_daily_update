#! /usr/bin/python
import os
import sys

def process_files(directory):
    meme_line = None
    alphabet_line = None
    strands_line = None
    bkg_freq = None
    motifs = {}

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as infile:
                while True:
                    line = infile.readline()
                    if not line:
                        break
                    splitline = line.split()
                    if line.startswith('MEME version') and not meme_line:
                        meme_line = line
                    if line.startswith('ALPHABET') and not alphabet_line:
                        alphabet_line = line
                    if line.startswith('strands:') and not strands_line:
                        strands_line = line
                    if line.startswith('Background letter frequencies') and not bkg_freq:
                        next_line = infile.readline()
                        if next_line:  # Ensure there is a next line
                            bkg_freq = next_line.strip()  # Set bkg_freq to the next line's content
                    if line.startswith('MOTIF'):
                        motif_name = "MOTIF" + " " + line.strip().split()[1]  # Assuming motif name is in the second word
                        if motif_name not in motifs:
                            motifs[motif_name] = []
                        motifs[motif_name].append(motif_name)
                        matrix_lines = []
                        while True:
                            if line.startswith('letter-probability matrix:'):# or ('log-odds matrix'):
                                matrix_lines.append(line)
                                while True:
                                    next_line = infile.readline()
                                    if len(next_line.split()) != 4:
                                        break
                                    matrix_lines.append(next_line.rstrip())  # Remove trailing newline character
                                motifs[motif_name].extend(matrix_lines)
                                break
                            else:
                                line = infile.readline()

    # Writing to the output file
    with open('combined_output_meme.txt', 'w') as outfile:
        outfile.write(meme_line + '\n')
        outfile.write(alphabet_line + '\n')
        outfile.write(strands_line + '\n')
        outfile.write(bkg_freq + '\n\n')

        for motif_name, lines in motifs.items():
    		# Join the lines while filtering out empty lines within the motif section
    		formatted_lines = '\n'.join(line.strip() for line in lines if line.strip())
    
   			# Check if there are any non-empty lines before writing to the file
    		if formatted_lines:
        		outfile.write(formatted_lines + '\n\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py directory_path")
    else:
        directory_path = sys.argv[1]
        process_files(directory_path)
