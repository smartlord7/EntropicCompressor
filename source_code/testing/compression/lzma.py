from source_code.cmp.modules.compression import lzma as lzma, lzw as lzw
import matplotlib.image as img
import os

#region Constants

FILES_DIR = '../resources/images/uncompressed/original/'

#endregion Constants


def analyse_files(files_dir):
    """
        Function for testing purposes. The files in the specified folder (.bmp images)
        will be compressed via LZMA encoding and then written in the current directory with the extension .lzma.
        :param files_dir: the directory in which the .bmp images are.
        :return:
    """
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp'):
                print('Compressing %s...' % file)
                image_data = img.imread(files_dir + '\\' + file).ravel()
                lzma_file = lzma.open(file.replace('.bmp', '.lzma.py'), 'wb')
                lzma_file.write(image_data)
                lzma_file.close()

def main():
    """
    Driver Program - for testing purposes -  Lempel Ziv Markov Encoding
    """
    if __name__ == '__main__':
       analyse_files(FILES_DIR)


main()