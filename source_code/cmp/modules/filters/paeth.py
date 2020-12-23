"""------------CODEC's nao destrutivos para imagens monocromaticas------------
Universidade de Coimbra
Licenciatura em Engenharia Informatica
Teoria da Informacao
Segundo ano, primeiro semestre

Authors:
João Afonso Vieira de Sousa, 2019224599, uc2019224599@student.uc.pt
José Domingos da Silva, 2018296125, uc2018296125@student.uc.pt
Sancho Amaral Simões, 2019217590, uc2019217590@student.uc.pt
Tiago Filipe Santa Ventura, 2019243695, uc2019243695@student.uc.pt

19/12/2020
---------------------------------------------------------------------------"""

import numpy as np

#region Private Functions


def __paeth_simplified_predictor(data, line, column):
    """
    Function that computes the Paeth simplified predictor (P = A + C - B) of a certain pixel in an image.
    :param data: the matrix tha represents the image.
    :param line: the line of the pixel.
    :param column: the column of the pixel.
    :return: the Paeth simplified predictor of the pixel in question.
    """
    left = data[line][column - 1]
    above = data[line - 1][column]
    upper_left = data[line - 1][column - 1]
    return left + above - upper_left


def __get_left_matrix(data):
    """
    Function that computes, using NumPy functions, the matrix of each image pixel's correspondent previous (left) pixel.
    :param data: the matrix that represents the image.
    :return: the matrix of each image pixel's correspondent previous (left) pixel.
    """
    return np.hstack((np.zeros((data.shape[0], 1)),
                      np.vstack((np.zeros(data.shape[1] - 1),
                                 np.delete(np.delete(data, 0, axis=0),
                                           data.shape[1] - 1, axis=1))))).astype(np.int16)


def __get_above_matrix(data):
    """
    Function that computes, using NumPy functions, the matrix of each image pixel's correspondent above pixel.
    :param data: the matrix that represents the image.
    :return: the matrix of each image pixel's correspondent above pixel.
    """
    return np.hstack((np.zeros((data.shape[0], 1)),
                      np.vstack(((np.zeros(data.shape[1] - 1)),
                                 np.delete(np.delete(data,
                                                     data.shape[0] - 1, axis=0), 0, axis=1))))).astype(np.int16)


def __get_upper_left_matrix(data):
    """
    Function that computes, using NumPy functions, the matrix of each image pixel's correspondent upper left pixel.
    :param data: the matrix that represents the image.
    :return: the matrix of each image pixel's correspondent upper left pixel.
    """
    return np.hstack((np.zeros((data.shape[0], 1)),
                      np.vstack((np.zeros(data.shape[1] - 1),
                                 np.delete(np.delete(data, data.shape[0] - 1, axis=0),
                                           data.shape[1] - 1, axis=1))))).astype(np.int16)

#endregion Private Functions

#region Public Functions


def apply_simplified_paeth_filter(data, width, height):
    """
    Function that applies, using NumPy matrices, the Simplified Paeth Prediction Method to each image's pixel.
    :param data: the matrix that represents the image.
    :param width: the image's width.
    :param height: the image's height.
    :return: the filtered matrix.
    """
    data = np.array(data).reshape((width, height)).astype(np.int16)
    left = __get_left_matrix(data)
    above = __get_above_matrix(data)
    upper_left = __get_upper_left_matrix(data)
    p = left + above - upper_left

    return (data - p).astype(np.uint8)#.astype(np.int16)


def invert_simplified_paeth_filter(data, width, height):
    """
    Function that applies, using NumPy matrices, the Inverse Simplified Paeth Prediction Method to each image's pixel
    :param data: the flattened array that represents the image.
    :param width: the image's width.
    :param height: the image's height.
    :return: the unfiltered image.
    """
    data = np.array(data).reshape((width, height)).astype(np.uint8)
    for i in range(1, data.shape[0]):
        for j in range(1, data.shape[1]):
            data[i][j] += __paeth_simplified_predictor(data, i, j)
    return data.astype(np.uint8)


def apply_paeth_filter(data, width, height, encode=True):
    """
    Experimental function! Not working properly!
    Since using the Paeth filter in a large image with Python is slow,
    an attempt of implementation of the Paeth filter using exclusively NumPy matricial operations was made.
    :param data: the matrix that represents the image.
    :param width: the image's width.
    :param height: the image's height.
    :param encode: flag that specifies whether the matrix should be filtered or unfiltered.
    :return: the filtered/unfiltered matrix.
    """
    data = np.array(data).reshape((width, height)).astype(np.int16)
    left = __get_left_matrix(data)
    above = __get_above_matrix(data)
    upper_left = __get_upper_left_matrix(data)
    p = left + above - upper_left
    dist_left = np.abs(p - left)
    dist_above = np.abs(p - above)
    dist_upper_left = np.abs(p - upper_left)
    predictor_left = data - left if encode else data + left
    predictor_above = data - above if encode else data + above
    predictor_upper_left = data - upper_left if encode else data + upper_left
    data_copy = np.where(np.logical_and(dist_left <= dist_above, dist_left <= dist_upper_left), predictor_left, data)
    data_copy = np.where(np.logical_and(dist_above <= dist_left, dist_above <= dist_upper_left), predictor_above, data)
    data_copy = np.where(np.logical_and(dist_upper_left <= dist_above, dist_upper_left <= dist_left), predictor_upper_left, data)
    return data_copy.astype(np.uint8)

#endregion Public Functions