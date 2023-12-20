#! /usr/bin/python
import os
import sys

def extract_headers(file_content):
    header_keywords = ["MEME version", "ALPHABET", "strands", "Background letter frequencies"]
    headers = []
    add_to_headers = False

    for i, line in enumerate(file_content):
        for keyword in header_keywords:
            if line.startswith(keyword):
                add_to_headers = True
                headers.append(line.strip())
                if i < len(file_content) - 1:  # Check if there's a line below
                    headers.append(file_content[i + 1].strip())  # Add the line below
                break
        if add_to_headers and line.startswith("Background letter frequencies"):
            break

    return headers

def extract_motifs(file_content):
    motifs = []
    add_to_motifs = False

    for line in file_content:
        if line.startswith("MOTIF"):
            add_to_motifs = True
        if add_to_motifs:
            if line.startswith("Time"):
                break
            motifs.append(line.strip())

    return motifs

def concatenate_files(directory):
    final_output = []  # Define final_output in the global scope
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    headers_added = False

    for file_name in files:
        with open(os.path.join(directory, file_name), 'r') as file:
            content = file.readlines()
            headers = extract_headers(content)
            if not headers_added:
                final_output.extend(headers)
                final_output.extend(["", ""])
                headers_added = True

            motifs = extract_motifs(content)
            final_output.extend(["*" * 80,"", "", "*" * 80])
            final_output.extend(motifs)
            final_output.extend(["", ""])

    return final_output  # Return the final_output list

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <directory_path> <output_file_name>")
        sys.exit(1)

    directory_path = sys.argv[1]
    output_file_name = sys.argv[2]

    final_output = concatenate_files(directory_path)

    # Adding the final line of asterisks to the end of the final output
    final_output.append("*" * 80)

    with open(output_file_name, 'w') as final_file:
        final_file.write('\n'.join(final_output))
