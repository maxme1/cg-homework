from collections import namedtuple, Counter
from queue import PriorityQueue
from typing import Dict, Any


class Node(namedtuple('Node', ['left', 'right'])):
    def __lt__(self, other):
        return isinstance(other, Node)

    def __gt__(self, other):
        return not self < other


def build_tree(frequencies: Dict[Any, float]):
    nodes = PriorityQueue()
    for value, freq in frequencies.items():
        nodes.put((freq, value))

    while nodes.qsize() > 1:
        (freq1, node1), (freq2, node2) = nodes.get(), nodes.get()
        nodes.put((freq1 + freq2, Node(node2, node1)))

    return nodes.get()[1]


def build_mapping(root: Node) -> Dict[Any, str]:
    mapping = {}

    def builder(node: Node, prefix: str):
        if isinstance(node, Node):
            builder(node.left, prefix + '1')
            builder(node.right, prefix + '0')
        else:
            mapping[node] = prefix

    builder(root, '')
    return mapping


def pack_bytes(bits: str):
    tail = len(bits) % 8
    if tail:
        padding = 8 - tail
    else:
        padding = 0

    bits += '0' * padding
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)), padding


def encode_with_mapping(text: bytes, mapping: Dict[int, str]):
    for b in text:
        yield from mapping[b]


def encode(text: bytes):
    tree = build_tree(Counter(text))
    mapping = build_mapping(tree)
    return (*pack_bytes(''.join(map(mapping.__getitem__, text))), tree)


def iterate_bits(number):
    bit = 128
    while bit:
        yield number & bit
        bit >>= 1


def _decode(text: bytes, padding: int, root: Node):
    node = root
    end_pointer = 8 - padding
    for i, byte in enumerate(text):
        for j, bit in enumerate(iterate_bits(byte)):
            if i == len(text) - 1 and j == end_pointer:
                return

            if bit:
                node = node.left
            else:
                node = node.right
            if not isinstance(node, Node):
                yield node
                node = root


def decode(text: bytes, padding: int, root: Node):
    return bytes(_decode(text, padding, root))
