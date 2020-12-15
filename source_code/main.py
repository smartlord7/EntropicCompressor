from matplotlib.mathtext import Filll

import source_code.filters as filt
import source_code.rle2 as rle
from lib.huffmancodec import HuffmanCodec, _EndOfFileSymbol
import lib.encoding_file_writer as frw
import os
import matplotlib.image as img


TO_COMPRESS_PATH = '../resources/images/uncompressed/'
TO_UNCOMPRESS_PATH = '../resources/images/compressed/generations/generation1/'
ESCAPE_CHARACTER = -256
EOF_SYMBOL = _EndOfFileSymbol()
table = None


def compress_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('bmp') or file.endswith('jpg'):
                print('Compressing %s...' % file)
                print('Applying Delta Encoding and RLE...')
                image_data = rle.rle_encode(filt.apply_subtraction_filter(img.imread(files_dir + '\\' + file).flatten()))

                print('Applying Huffman Encoding...')
                global table
                table = HuffmanCodec.from_data(image_data).get_code_table()
                image_data = frw.encode(image_data, table, EOF_SYMBOL)
                frw.write_file(TO_UNCOMPRESS_PATH + file[:len(file) - 4] + '.cmp', image_data)
                print('--------')


def uncompress_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('cmp'):
                print('Uncompressing %s...' % file)
                data = frw.read_file(TO_UNCOMPRESS_PATH + file)
                print('Applying inverse Huffman Encoding...')
                data = frw.decode(data, table, EOF_SYMBOL)
                print('Applying inverse RLE...')
                data = rle.rle_decode(data, ESCAPE_CHARACTER)
                print('Applying inverse Delta Encoding')
                data = filt.decode_subtraction_filter(data, ESCAPE_CHARACTER, transpose=True)
                print(data)
                print('--------')

def main():
    if __name__ == '__main__':
        compress_files(TO_COMPRESS_PATH)
        uncompress_files(TO_UNCOMPRESS_PATH)

main()