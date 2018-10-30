import argparse
from huffman import encode_to_file

parser = argparse.ArgumentParser()
parser.add_argument('input', help='path to input text file.')
parser.add_argument('output', help='path to output binary file.')
args = parser.parse_args()

with open(args.input) as file:
    encode_to_file(file.read(), args.output)
