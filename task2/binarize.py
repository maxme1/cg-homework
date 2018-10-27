import imageio

from utils import *


def global_thresholding(image):
    return 255 * (image > 127)


def random_dithering(image):
    return 255 * (image > np.random.randint(256, size=image.shape))


def ordered_dithering(image, order=2):
    matrix = 256 * make_dithering_matrix(order)
    scale = np.ceil(np.array(image.shape) / matrix.shape).astype(int)
    tiles = np.tile(matrix, scale)

    return image > tiles[build_slices([0, 0], image.shape)]


def row_diffusion(row):
    row = row.copy().astype(int)
    for i in range(len(row)):
        old_value = row[i]
        row[i] = global_thresholding(old_value)
        if i < len(row) - 1:
            row[i + 1] += old_value - row[i]

    return row.astype('uint8')


def error_diffusion(image):
    return np.stack(map(row_diffusion, image))


def bidirectional_error_diffusion(image):
    result = np.empty_like(image)
    result[:, ::2] = error_diffusion(image[:, ::2])
    result[:, 1::2] = error_diffusion(image[:, 1::2][:, ::-1])[:, ::-1]
    return result


def floyd_steinberg(image):
    image = image.copy().astype(float)
    shape = np.array(image.shape) - [1, 2]
    for x, y in np.ndindex(*shape):
        idx = (x, y + 1)
        window_start = np.array([x, y], int)

        old_value = image[idx]
        image[idx] = global_thresholding(old_value)
        error = old_value - image[idx]

        slc = build_slices(window_start, window_start + FS_MATRIX.shape)
        image[slc] += FS_MATRIX * error

    return global_thresholding(image)


CHOICES = {
    'thresholding': global_thresholding,
    'random_dithering': random_dithering,
    'ordered_dithering': ordered_dithering,
    'error_diffusion': error_diffusion,
    'bidirectional_error_diffusion': bidirectional_error_diffusion,
    'floyd_steinberg': floyd_steinberg,
}

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=CHOICES, help='the binarization mode.')
    parser.add_argument('input', help='path to the input image.')
    parser.add_argument('output', help='path to the output image.')
    args = parser.parse_args()

    imageio.imsave(
        CHOICES[args.mode](args.output),
        imageio.imread(args.input)
    )
