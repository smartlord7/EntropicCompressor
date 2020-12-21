import source_code.cmp.modules.compression.lzw as lzw
import matplotlib.image as img
import os


FILES_DIR = '../resources/images/uncompressed/original/'


def analyse_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp'):
                image_data = img.imread(files_dir + '\\' + file).ravel()
                image_data_encoded = lzw.lzw_encode(image_data, 4096, True)
                print(image_data_encoded)


def main():
    if __name__ == '__main__':
        string = [0, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 2, 3, 1, 3, 1, 2, 3, 2, 1, 2, 1, 3, 2, 1, 3, 2, -1, -1, -1, -1]
        print(string)
        alphabet = [-1, 0, 1, 2, 3]
        encoded = lzw.lzw_encode(string, alphabet)
        print(encoded)
        decoded = lzw.lzw_decode(encoded, alphabet)
        print(decoded)
        #analyse_files(FILES_DIR)


main()