import numpy as np
import matplotlib.image as img
import os


def lzw_encode(data, min, max):
    num_elements = abs(max) + abs(min) + 1
    entries = {(i, ): i for i in range(num_elements)}
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
    num_elements = abs(max) + abs(min) + 1
    entries = {i: (i,) for i in range(num_elements)}
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


FILES_DIR = '../resources/images/uncompressed_images/'


def analyse_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp') or file.endswith('.jpg'):
                image_data = img.imread(files_dir + '\\' + file)
                image_data = image_data.flatten()
                image_data_encoded = lzw_encode(image_data, 0, 255)
                print(len(image_data_encoded))


def main():
    if __name__ == '__main__':
        """string = [1, 3, 2, 1, 3, 2, 5, 2, 4, 2, 4, 1, 7, 3, 1, 7, 3, 1, 3, 2]
        encoded = lzw_encode(string, 1, 7)
        decoded = lzw_decode(encoded, 1, 7)
        print(encoded)
        print(decoded)"""
        analyse_files(FILES_DIR)


main()