from lib import entropic_encoding as ec
import matplotlib.image as img
import os

GROUP_SIZE = 2
FILES_DIR = 'C:\\Users\\Sancho\\PycharmProjects\\TI\TP2\\resources\\images\\uncompressed_images'
TICKS_SIZE = 10


def analyse_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp'):
                image_data = img.imread(files_dir + '\\' + file)
                image_data = image_data.flatten()
                alphabet = ec.gen_alphabet(image_data)
                histogram = ec.gen_histogram(image_data, len(alphabet))
                histogram_pairs, num_groups = ec.gen_histogram_generic(image_data, GROUP_SIZE)
                ec.plot_histogram(alphabet, histogram, file, TICKS_SIZE)
                print('Entropy (groups of one symbol): %.4f  bits\n'
                      'Entropy (groups of two symbols) : %.4f  bits'
                      % (ec.entropy(histogram, len(image_data)),
                         ec.entropy_generic(histogram_pairs, num_groups, GROUP_SIZE)))


def main():
    if __name__ == '__main__':
        analyse_files(FILES_DIR)


main()
