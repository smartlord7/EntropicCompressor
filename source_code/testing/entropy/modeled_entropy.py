from source_code.cmp.modules.filters import subup as sub, paeth as paeth
from source_code.cmp.modules.transforms import mtf as mtf
import source_code.cmp.modules.util.entropy as ec
import matplotlib.image as img
import warnings
import numpy as np
import os

#region Constants

FILES_DIR = '../../../resources/images/decompressed/original/'

#endregion Constants

#region Public Functions


def analyse_files(files_dir):
    """
    Function for testing purposes. The files in the specified folder (.bmp images)
    will be analysed in order to retrieve their base entropy, their entropy when up filter is applied, their entropy
    when the simple Paeth filter is applied and their entropy when the MTF transform is applied (Move To Front).
    :param files_dir: the directory in which the .bmp images are.
    :return:
    """
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp'):
                image_data = img.imread(files_dir + file)

                l_shape = len(image_data.shape)
                if l_shape == 3:
                    image_data = image_data[:, :, 0]

                alphabet = [i for i in range(0, 256)]

                image_data_up = sub.apply_simple_filter(image_data, up=True)
                image_data_sub = sub.apply_simple_filter(image_data, up=False)
                image_data_paeth = paeth.apply_simplified_paeth_filter(image_data, len(image_data), len(image_data[0]))

                image_data_raveled = image_data.ravel()
                image_data_mtf = mtf.apply_mtf(image_data_raveled, alphabet)

                len_data = len(image_data) * len(image_data[0])

                histogram = np.array(np.unique(image_data_raveled, return_counts=True))
                histogram_up = np.array(np.unique(image_data_up, return_counts=True))
                histogram_sub = np.array(np.unique(image_data_sub, return_counts=True))
                histogram_paeth = np.array(np.unique(image_data_paeth.ravel(), return_counts=True))
                histogram_mtf = np.array(np.unique(image_data_mtf, return_counts=True))

                ec.plot_histogram(histogram_up[0], histogram_up[1], title='%s (Up Filter)' % file, ticks_size=10)
                ec.plot_histogram(histogram_sub[0], histogram_sub[1], title='%s (Sub Filter)' % file, ticks_size=10)
                ec.plot_histogram(histogram_paeth[0], histogram_paeth[1], title='%s (Paeth Simplified Filter)' % file, ticks_size=10)
                ec.plot_histogram(histogram_mtf[0], histogram_mtf[1], title='%s (MTF)' % file, ticks_size=10)
                #histogram_grouped, num_groups = ec.gen_histogram_generic(image_data_up, 2)

                print('%s:\nEntropy (with no filters): %.4f bits\n'
                      'Entropy (with up filter) : %.4f bits\n'
                      'Entropy (with sub filter) : %.4f bits\n'
                        'Entropy (with simplified paeth filter) : %.4f bits\n'
                        'Entropy (with mtf transform) : %.4f bits\n'
                        %   (file, ec.entropy(histogram[1], len_data),
                            ec.entropy(histogram_up[1], len_data),
                             ec.entropy(histogram_sub[1], len_data),
                            ec.entropy(histogram_paeth[1], len_data),
                            ec.entropy(histogram_mtf[1], len_data)))


def main():
    """
    Driver program for testing purposes - No filters, Up Filter, Simplified Paeth Filter and MTF Transform.
    """
    if __name__ == '__main__':
        warnings.filterwarnings('ignore')
        analyse_files(FILES_DIR)


#endregion Public Functions


main()