import numpy as np
from cffi.backend_ctypes import xrange

import lib.entropic_encoding as ec


def bwt_encode(data):
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
    if type(encoded_data) == np.ndarray:
        l = len(encoded_data)
        original_matrix = np.zeros((l, l))
        for i in range(l):
            original_matrix[i] = encoded_data[i]
            original_matrix.sort()
        return original_matrix[index].astype(np.int32)


def ord_array_to_string(ord_array):
    string = str()
    for element in ord_array:
        string += chr(element)
    return string


def suffix_array(data):
    satups = sorted([(list(data[i:]), i) for i in xrange(0, len(data))])
    return map(lambda x: x[1], satups)


def bwt_via_suffix_array(data):
    bw_encoded = list()
    for suffix in suffix_array(data):
        if not suffix:
            bw_encoded.append('$')
        else:
            bw_encoded.append(data[suffix - 1])
    return bw_encoded


def rank_bwt(encoded_data):
    tots = dict()
    ranks = list()
    for character in encoded_data:
        tots.setdefault(character, 0)
        ranks.append(tots[character])
        tots[character] += 1
    return ranks, tots


def first_col(tots):
    first = dict()
    tot_characters = int()
    for character, count in sorted(tots.items()):
        first[character] = (tot_characters, tot_characters + count)
        tot_characters += count
    return first


def reverse_bwt(encoded_data):
    ranks, tots = rank_bwt(encoded_data)
    first = first_col(tots)
    row_index = int()
    decoded = ['$']
    while encoded_data[row_index] != '$':
        character = encoded_data[row_index]
        decoded = [character] + decoded
        row_index = first[character][0] + ranks[row_index]
    return decoded


def main():
    if __name__ == '__main__':
        data ='dasfasdaadsadasdsdsdsadasdwqeqwewqeeqwesadafafwrwwwfewfsd$s'
        bw_encoded = bwt_via_suffix_array(data)
        bw_decoded = reverse_bwt(bw_encoded)

main()