import pickle
import argparse
from huffman import encode

parser = argparse.ArgumentParser()
parser.add_argument('input', help='path to input text file.')
parser.add_argument('output', help='path to output binary file.')
args = parser.parse_args()

with open(args.input, 'rb') as in_, open(args.output, 'wb') as out:
    pickle.dump(encode(in_.read()), out)
