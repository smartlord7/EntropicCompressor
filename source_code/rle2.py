import source_code.filters as filters
import matplotlib.image as img
import os
from lib.huffmancodec import HuffmanCodec
from lib.huffmancodec import _EndOfFileSymbol
import lib.encoding_file_writer as fw
import numpy as np


def rle_encode(data, escape_character=-256):
    encoded_data = list()
    length = len(data)
    i = int()
    while i < length:
        if not i % 1000000:
            print("%.2f %%" % (i / length * 100))
        if i == length - 1:
            encoded_data.append(data[i])
            break
        current = data[i]
        nextIndex = i + 1
        next = data[nextIndex]
        while current == next:
            nextIndex += 1
            if nextIndex >= length:
                break
            next = data[nextIndex]
        if nextIndex - i > 3:
            encoded_data.append(escape_character)
            encoded_data.append(current)
            encoded_data.append(nextIndex - i)
        else:
            for i in range(nextIndex - i):
                encoded_data.append(current)
        i = nextIndex
    eof_symbol = _EndOfFileSymbol()
    encoded_data.append(eof_symbol)
    return encoded_data


def rle_decode(encoded_data, escape_character=-256):
    decoded_data = list()
    length = len(encoded_data)
    i = int()
    while i < length:
        current = encoded_data[i]
        if current == escape_character:
            character = encoded_data[i + 1]
            times = encoded_data[i + 2]
            for j in range(times):
                decoded_data.append(character)
            i += 3
        else:
            decoded_data.append(current)
            i += 1
    return decoded_data


FILES_DIR = '../resources/images/uncompressed/'


def analyse_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('bmp') or file.endswith('jpg'):
                print('Compressing %s...' % file)
                image_data = rle_encode(filters.apply_subtraction_filter(img.imread(files_dir + '\\' + file).flatten()))
                eof_symbol = _EndOfFileSymbol()
                image_data.append(eof_symbol)
                table = HuffmanCodec.from_data(image_data).get_code_table()
                image_data = fw.encode(image_data, table, eof_symbol)
                fw.write_file(file[:len(file) - 4], image_data)
                print('--------')



def main():
    if __name__ == '__main__':
        """string = np.array([2, 2, 2, 2, 3, 3, 3, 3, 1])
        encoded = rle_encode(string)
        print(encoded)
        decoded = rle_decode(encoded)
        print(decoded)"""
        analyse_files(FILES_DIR)


main()
