import argparse
from huffman import decode_from_file

parser = argparse.ArgumentParser()
parser.add_argument('input', help='path to input binary file.')
parser.add_argument('output', help='path to output text file.')
args = parser.parse_args()

with open(args.output, 'w') as file:
    file.write(decode_from_file(args.input))
