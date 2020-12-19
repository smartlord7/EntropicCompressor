from source_code.cmp.modules.filters import sub as sub, paeth as paeth
import lib.entropic_encoding as ec
import matplotlib.image as img
import warnings
import numpy as np
import os

FILES_DIR = '../../resources/images/uncompressed/original/'


def analyse_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp'):
                image_data = img.imread(files_dir + file)
                l_shape = len(image_data.shape)
                if l_shape == 3:
                    image_data = image_data[:, :, 0]
                image_data_sub = sub.apply_simple_filter(image_data.ravel(), up=True)
                image_data_paeth = paeth.apply_paeth_filter(image_data)
                len_data = len(image_data) * len(image_data[0])
                histogram = np.array(np.unique(image_data, return_counts=True))[1]
                histogram_sub = np.array(np.unique(image_data_sub, return_counts=True))[1]
                histogram_paeth = np.array(np.unique(image_data_paeth.ravel(), return_counts=True))[1]
                #histogram_grouped, num_groups = ec.gen_histogram_generic(image_data_sub, 2)
                print('%s:\nEntropy (with no filters): %.4f bits\n'
                      'Entropy (with subtraction filter) : %.4f bits\n'
                      'Entropy (with paeth filter) : %.4f bits\n'
                      % (file, ec.entropy(histogram, len_data),
                         ec.entropy(histogram_sub, len_data),
                         ec.entropy(histogram_paeth, len_data)))


def main():
    if __name__ == '__main__':
        warnings.filterwarnings('ignore')
        analyse_files(FILES_DIR)


main()