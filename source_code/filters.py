import numpy as np
import lib.entropic_codification as ec
import matplotlib.image as img
import os


def to_numpy_int8(data):
    if type(data) != np.ndarray:
        data = np.array(list(data))
    if data.dtype != np.int8:
        data = data.astype(np.int8)
    return data


def apply_subtraction_filter(data, subtract_previous=True):
    data = to_numpy_int8(data)
    if subtract_previous:
        data_copy = np.delete(data.copy(), len(data) - 1)
        data_copy = np.concatenate(([0], data_copy))
    else:
        data_copy = np.delete(data, 0)
        data_copy = np.concatenate((data_copy, [0]))
    return data - data_copy


def decode_subtraction_filter(data, subtract_previous=True):
    data = to_numpy_int8(data)
    l = len(data)
    if subtract_previous:
        for i in range(1, l):
            data[i] = data[i] + data[i - 1]
    else:
        for i in range(1, l):
            data[i - 1] = data[i - 1] + data[i]
    return data


FILES_DIR = 'C:\\Users\\Sancho\\PycharmProjects\\TI\TP2\\resources\\images\\uncompressed_images'


def analyse_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp') or file.endswith('.jpg'):
                image_data = img.imread(files_dir + '\\' + file)
                image_data = image_data.flatten()
                image_data_filtered = apply_subtraction_filter(image_data)
                alphabet = ec.gen_alphabet(image_data)
                len_data = len(image_data)
                len_alphabet = len(alphabet)
                histogram = ec.gen_histogram(image_data, len_alphabet)
                histogram_filtered = ec.gen_histogram(image_data_filtered, len_alphabet)
                print('Entropy (without subtraction filter): %.4f bits\n'
                      'Entropy (with subtraction filter) : %.4f bits'
                      % (ec.entropy(histogram, len_data),
                         ec.entropy(histogram_filtered, len_data)))


def main():
    if __name__ == '__main__':
        analyse_files(FILES_DIR)


main()