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
from cffi.backend_ctypes import xrange

#region Public Functions


def bwt_encode(data):
    """
    Naive implementation of Burrows-Wheeler Transform that supports numpy.
    :param data: the target data.
    :return: the BWT encoded data and the index of the original string in the rotation matrix.
    """
    if type(data) == np.ndarray:
        l = len(data)
        rotation_matrix = np.zeros((l, l))
        current = np.zeros(l)
        if type(data[0]) == np.str_:
            for i in range(l):
                current[i] = ord(data[i])
        original_string = current
        for i in range(l):
            current = np.append(current[l - 1], current[0:l - 1])
            rotation_matrix[i] = current
        rotation_matrix = rotation_matrix[np.lexsort(np.rot90(rotation_matrix))]
        bwt_encoded = np.array(list())
        original_word_index = int()
        for i in range(l):
            if (rotation_matrix[i] == original_string).all():
                original_word_index = i
            bwt_encoded = np.append(bwt_encoded, rotation_matrix[i][l - 1])
        return bwt_encoded.astype(np.int32), original_word_index


def bwt_decode(encoded_data, index):
    """
    Naive implementation of Burrows-Wheeler Inverse Transform.
    :param encoded_data: the target data.
    :return: the BWT decoded data.
    """
    if type(encoded_data) == np.ndarray:
        l = len(encoded_data)
        original_matrix = np.zeros((l, l))
        for i in range(l):
            original_matrix[i] = encoded_data[i]
            original_matrix.sort()
        return original_matrix[index].astype(np.int32)


def suffix_array(data):
    """
    Util function that generates a lexicographically ordered sufix array of the target data.
    :param data: the target data.
    :return: the lexicographically ordered sufix array of the target data.
    """
    satups = sorted([(list(data[i:]), i) for i in xrange(0, len(data))])
    return map(lambda x: x[1], satups)


def bwt_via_suffix_array(data):
    """
    Function that encodes a given piece of data using the BWT Transform via suffix array
    :param data: the target data.
    :return: the BWT encoded data.
    """
    bw_encoded = list()
    for suffix in suffix_array(data):
        if not suffix:
            bw_encoded.append('$')
        else:
            bw_encoded.append(data[suffix - 1])
    return bw_encoded


def rank_bwt(encoded_data):
    """
    Util function that t-ranks a BWT encoded data so it can be decoded.
    Each character will have a rank index that equals to the previous ocurrences of that same character in the given data.
    :param encoded_data: the bwt encoded data.
    :return:
    """
    tots = dict()
    ranks = list()
    for character in encoded_data:
        tots.setdefault(character, 0)
        ranks.append(tots[character])
        tots[character] += 1
    return ranks, tots


def first_col(tots):
    """
    Util function used in BWT that retrieves the first column of the rotation matrix.
    :param data: the target data.
    :return: the BWT decoded data.
    """
    first = dict()
    tot_characters = int()
    for character, count in sorted(tots.items()):
        first[character] = (tot_characters, tot_characters + count)
        tot_characters += count
    return first


def reverse_bwt(encoded_data):
    """
    Function that decodes a given piece of data using the BWT Transform via suffix array
    :param data: the target data.
    :return: the BWT decoded data.
    """
    ranks, tots = rank_bwt(encoded_data)
    first = first_col(tots)
    row_index = int()
    decoded = ['$']
    while encoded_data[row_index] != '$':
        character = encoded_data[row_index]
        decoded = [character] + decoded
        row_index = first[character][0] + ranks[row_index]
    return decoded


#endregion Public Functions