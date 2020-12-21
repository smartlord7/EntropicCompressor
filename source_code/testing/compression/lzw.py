import source_code.cmp.modules.compression.lzw as lzw
import matplotlib.image as img
import os

#region Constants

FILES_DIR = '../resources/images/uncompressed/original/'

#endregion Constants

#region Public Functions


def analyse_files(files_dir):
    """
    Function for testing purposes. The files in the specified folder (.bmp images)
    will be compressed via LZW encoding to memory.
    :param files_dir: the directory in which the .bmp images are.
    :return:
    """
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp'):
                image_data = img.imread(files_dir + '\\' + file).ravel()
                image_data_encoded = lzw.lzw_encode(image_data, 4096, True)
                print(image_data_encoded)


def main():
    """
    Driver Program for testing purposes - LZW Encoding
    """
    if __name__ == '__main__':
        string = [0, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 2, 3, 1, 3, 1, 2, 3, 2, 1, 2, 1, 3, 2, 1, 3, 2, -1, -1, -1, -1]
        print(string)
        alphabet = [-1, 0, 1, 2, 3]
        encoded = lzw.lzw_encode(string)
        print(encoded)
        decoded = lzw.lzw_decode(encoded)
        print(decoded)
        #analyse_files(FILES_DIR)


#endregion Public Functions


main()