import pickle
from collections import namedtuple, Counter
from queue import PriorityQueue
from typing import Dict


class Node(namedtuple('Node', ['frequency', 'left', 'right', 'value'])):
    def __lt__(self, other):
        return isinstance(other, Node) and self.frequency < other.frequency


def build_tree(frequencies: Dict[bytes, float]):
    nodes = PriorityQueue()
    for value, freq in frequencies.items():
        nodes.put(Node(freq, None, None, value))

    while nodes.qsize() > 1:
        node1, node2 = nodes.get(), nodes.get()
        nodes.put(Node(node1.frequency + node2.frequency, node2, node1, None))

    return nodes.get()


def build_mapping(root: Node) -> Dict[bytes, str]:
    mapping = {}

    def builder(node: Node, prefix: str):
        if not isinstance(node, Node):
            return

        builder(node.left, prefix + '1')
        builder(node.right, prefix + '0')
        if node.value is not None:
            mapping[node.value] = prefix

    builder(root, '')
    return mapping


def find_symbol(text: bytes, root: Node):
    while root.value is None:
        if text[0] == '1':
            root = root.left
        else:
            root = root.right
        text = text[1:]

    return root.value, text


def to_bytes(s: str):
    return bytes(bytearray(int(s[x:x + 8], 2) for x in range(0, len(s), 8)))


def from_bytes(array: bytes):
    def pad(s):
        return '0' * (8 - len(s)) + s

    return ''.join(pad(bin(b)[2:]) for b in array)


def encode(text: bytes):
    tree = build_tree(Counter(text))
    encoded = ''.join(map(build_mapping(tree).__getitem__, text))
    return to_bytes(encoded), tree


def decode_with_tree(text: bytes, root: Node):
    result = b''
    text = from_bytes(text)
    while text:
        c, text = find_symbol(text, root)
        result += c
    return result
