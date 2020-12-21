import numpy as np


def paeth_predictor(data, line, column):
    left = data[line][column - 1]
    above = data[line - 1][column]
    upper_left = data[line - 1][column - 1]
    return left + above - upper_left


def __get_left_mattrix(data):
    return np.hstack((np.zeros((data.shape[0], 1)),
                      np.vstack((np.zeros(data.shape[1] - 1),
                                 np.delete(np.delete(data, 0, axis=0), data.shape[1] - 1, axis=1))))).astype(np.int16)


def __get_above_mattrix(data):
    return np.hstack((np.zeros((data.shape[0], 1)),
                      np.vstack(((np.zeros(data.shape[1] - 1)),
                                 np.delete(np.delete(data, data.shape[0] - 1, axis=0), 0, axis=1))))).astype(np.int16)


def __get_upper_left_mattrix(data):
    return np.hstack((np.zeros((data.shape[0], 1)),
                      np.vstack((np.zeros(data.shape[1] - 1),
                                 np.delete(np.delete(data, data.shape[0] - 1, axis=0),
                                           data.shape[1] - 1, axis=1))))).astype(np.int16)


def apply_simplified_paeth_filter(data, width, height):
    data = np.array(data).reshape((width, height)).astype(np.int16)
    left = __get_left_mattrix(data)
    above = __get_above_mattrix(data)
    upper_left = __get_upper_left_mattrix(data)
    p = left + above - upper_left

    return (data - p).astype(np.uint8)


def invert_simplified_paeth_filter(data, width, height):
    data = np.array(data).reshape((width, height)).astype(np.uint8)
    for i in range(1, data.shape[0]):
        for j in range(1, data.shape[1]):
            data[i][j] += paeth_predictor(data, i, j)
    return data.astype(np.uint8)


def apply_paeth_filter(data, width, height, encode=True):
    data = np.array(data).reshape((width, height)).astype(np.int16)
    left = __get_left_mattrix(data)
    above = __get_above_mattrix(data)
    upper_left = __get_upper_left_mattrix(data)
    p = left + above - upper_left
    dist_left = np.abs(p - left)
    dist_above = np.abs(p - above)
    dist_upper_left = np.abs(p - upper_left)
    data = data.astype(np.int16)
    predictor_left = data - left if encode else data + left
    predictor_above = data - above if encode else data + above
    predictor_upper_left = data - upper_left if encode else data + upper_left
    data_copy = np.where(np.logical_and(dist_left <= dist_above, dist_left <= dist_upper_left), predictor_left, data)
    data_copy = np.where(np.logical_and(dist_above <= dist_left, dist_above <= dist_upper_left), predictor_above, data)
    data_copy = np.where(np.logical_and(dist_upper_left <= dist_above, dist_upper_left <= dist_left), predictor_upper_left, data)
    return data_copy.astype(np.uint8)