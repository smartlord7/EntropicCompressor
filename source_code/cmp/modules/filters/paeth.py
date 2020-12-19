import source_code.cmp.modules.filters.util as util
import numpy as np


def paeth_predictor(data, line, column):
    left = data[line][column - 1]
    above = data[line - 1][column]
    upper_left = data[line - 1][column - 1]
    p = left + above - upper_left
    dist_left = abs(p - left)
    dist_above = abs(p - above)
    dist_upper_left = abs(p - upper_left)
    if dist_left <= dist_above and dist_left <= dist_upper_left:
        return left
    elif dist_above <= dist_left and dist_above <= dist_upper_left:
        return above
    else:
        return upper_left


def apply_paeth_filter(data):
    data_copy = np.array(data).astype(np.int16)
    for i in range(1, data.shape[0]):
        for j in range(1, data.shape[1]):
            util.show_progress(i * data.shape[1] + j, data.shape[0] * data.shape[1])
            predictor = paeth_predictor(data, i, j)
            data_copy[i][j] -= predictor
    return data_copy.astype(np.uint8)


def invert_paeth_filter(data, width, height):
    data = util.to_numpy_uint8(data).reshape(height, width)
    for i in range(1, data.shape[0]):
        for j in range(1, data.shape[1]):
            predictor = paeth_predictor(data, i, j)
            data[i][j] += predictor
    return data.astype(np.uint8)


def main():
    if __name__ == '__main__':
        width, height = 10, 10
        data = np.random.randint(0, 10, (width, height))
        print(data)
        filtered = apply_paeth_filter(data)
        print(filtered)
        decoded = invert_paeth_filter(filtered, width, height)
        print(decoded)
        print(data == decoded)

main()