import numpy as np
import matplotlib.image as img
from source_code import filters
import os


def lzw_encode(data, min, max):
    entries = {(i, ): i for i in range(min, max + 1)}
    dict_size = len(entries)
    current = tuple()
    encoded = list()
    for symbol in data:
        concat = current + (symbol, )
        if concat in entries:
            current += (symbol, )
        else:
            encoded.append(entries[current])
            entries[concat] = dict_size
            dict_size += 1
            current = (symbol, )
    if current:
        encoded.append(entries[current])
    return encoded


def lzw_decode(encoded_data, min, max):
    entries = {i: (i,) for i in range(min, max + 1)}
    dict_size = len(entries)
    decoded = list()
    current = (encoded_data[0], )
    encoded_data = np.delete(encoded_data, 0)
    decoded.append(current)
    for symbol in encoded_data:
        if symbol in entries:
            entry = entries[symbol]
        elif symbol == dict_size:
            entry = current + (current[0], )
        else:
            raise ValueError('Bad LZW compressed: %s!' % symbol)
        decoded.append(entry)
        entries[dict_size] = current + (entry[0], )
        dict_size += 1
        current = entry
    return decoded


def rle_encode(data):
    encoded = tuple()



FILES_DIR = '../resources/images/uncompressed_images/'


def analyse_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp') or file.endswith('.jpg'):
                image_data = img.imread(files_dir + '\\' + file)
                image_data = image_data.flatten()
                image_data_encoded = lzw_encode(image_data, 0, 255)
                with open('uncompressed_' + file.replace('bmp', ''), "wb") as uncompressed:
                    for symbol in image_data_encoded:
                        uncompressed.write(bytes(symbol))



def main():
    if __name__ == '__main__':
        #string = [-1, -2, -3, 1, 3, 2, 1, 3, 2, 5, 2, 4, 2, 4, 1, 7, 3, 1, 7, 3, 1, 3, 2, 1, 3, 2, 1, 3, 2]
        #encoded = lzw_encode(string, -3, 7)
        #decoded = np.array(lzw_decode(encoded, -3, 7)).flatten()
        #print(encoded)
        #print(decoded)
        analyse_files(FILES_DIR)


main()