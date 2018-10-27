import numpy as np

DITHERING_MATRIX = np.array([[0, 2], [3, 1]]) / 4
FS_MATRIX = np.array([[0, 0, 7], [3, 5, 1]]) / 16


def build_slices(start, stop):
    return tuple(map(slice, start, stop))


def make_dithering_matrix(order):
    if order < 2 or (order & (order - 1)) != 0:
        raise ValueError('Order must be a power of 2: %d' % order)

    if order == 2:
        return DITHERING_MATRIX

    area = order ** 2
    prev = area * make_dithering_matrix(order // 2)
    return np.concatenate([
        np.concatenate([prev, prev + 2], 1),
        np.concatenate([prev + 3, prev + 1], 1)
    ]) / area
