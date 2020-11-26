import numpy as np
import lib.entropic_codification as ec
import matplotlib.image as img
import os
import copy


def to_numpy_int8(data):
    if type(data) != np.ndarray:
        data = np.array(list(data))
    if data.dtype != np.int8:
        data = data.astype(np.int8)
    return data


def apply_subtraction_filter(data, subtract_previous=True, transpose=False):
    data_copy = to_numpy_int8(copy.deepcopy(data))
    if transpose:
        data_copy = np.transpose(data_copy)
    data_copy = data_copy.flatten()
    if subtract_previous:
        sub = np.delete(data_copy, len(data_copy) - 1)
        sub = np.concatenate(([0], sub))
    else:
        sub = np.delete(data, 0)
        sub = np.concatenate((sub, [0]))
    return data_copy - sub


def decode_subtraction_filter(data, subtract_previous=True, transpose=False):
    data = to_numpy_int8(data)
    data = data.flatten()
    l = len(data)
    if transpose:
        data = np.transpose(data)
    if subtract_previous:
        for i in range(1, l):
            data[i] = data[i] + data[i - 1]
    else:
        for i in range(1, l):
            data[i - 1] = data[i - 1] + data[i]
    return data


FILES_DIR = '../resources/images/uncompressed_images/'


def analyse_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp') or file.endswith('.jpg'):
                image_data = img.imread(files_dir + '\\' + file)
                image_data_filtered = apply_subtraction_filter(image_data, transpose=True)
                len_data = image_data.shape[0] * image_data.shape[1]
                histogram = np.array(np.unique(image_data, return_counts=True))[1]
                histogram_filtered = np.array(np.unique(image_data_filtered, return_counts=True))[1]
                histogram_grouped, num_groups = ec.gen_histogram_generic(image_data_filtered, 2)

                print('%s:\nEntropy (without subtraction filter): %.4f bits\n'
                      'Entropy (with subtraction filter) : %.4f bits\n'
                      'Entropy (with subtraction filter and pairs of symbols) : %.4f bits\n'
                      % (file, ec.entropy(histogram, len_data),
                         ec.entropy(histogram_filtered, len_data),
                         ec.entropy_generic(histogram_grouped, num_groups, 2)))


def main():
    if __name__ == '__main__':
        analyse_files(FILES_DIR)


main()