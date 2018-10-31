import pickle
import argparse
from huffman import decode

parser = argparse.ArgumentParser()
parser.add_argument('input', help='path to input binary file.')
parser.add_argument('output', help='path to output text file.')
args = parser.parse_args()

with open(args.input, 'rb') as in_, open(args.output, 'wb') as out:
    out.write(decode(*pickle.load(in_)))
