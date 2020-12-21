from source_code.cmp.modules.compression.huffmancodec import HuffmanCodec, _EndOfFileSymbol
from source_code.cmp.modules.filters import sub as sub, paeth as paeth
from source_code.cmp.modules.transforms import mtf as mtf
from source_code.cmp.modules.compression import lzw as lzw, rle as rle, lzma as lzma
import source_code.cmp.modules.util.encoding_file_writer as frw
from PIL import Image
import matplotlib.image as img
import numpy as np
import os
import time
import warnings

"""
    Exception throwed when trying to compress an image without .bmp extension
"""


class InvalidFileExtensionError(Exception):
    pass


"""
    Class that encapsulates the information about a custom .bmp compressor. The functions applied can be interchangeable
    in order to test different combinations of compression algorithms
"""


class BMPCompressor(object):

    #region Constants

    INITIAL_ALPHABET_LENGTH = 256
    ESCAPE_CHARACTER = -256
    EOF_SYMBOL = _EndOfFileSymbol()
    FILE_EXTENSION = '.cmp'
    ALPHABET = [i for i in range(256)]

    #endregion Constans

    #region Constructors

    def __init__(self, input_file_path, output_file_path, benchmark=False, log_data=False):
        """
        BMPCompressor Constructor
        :param input_file_path: the target file absolute/relative path
        :param output_file_path: the output file absolute/relative path
        :param benchmark: flag that toggles data exhibition about compression in each step
        :param log_data: flag that toggles the compressed data exhibition in each step
        """

        if not input_file_path.endswith('.bmp'):
            raise InvalidFileExtensionError

        matrix_data = img.imread(input_file_path)

        l_shape = len(matrix_data.shape)

        if l_shape == 3:
            matrix_data = matrix_data[:, :, 0]

        if log_data:
            print(matrix_data)

        self.__rle = False
        self.__input_file_path = input_file_path
        self.__output_file_path = output_file_path
        self.__file_name = self.__input_file_path.split('/')[::-1][0]

        self.__log_file = open(self.__output_file_path + self.__file_name.split('.')[0] + '_cmp_log.txt', 'w')
        self.__log_file.write('-------%s CMP COMPRESSION LOG-------\n\n'
                            'COMPRESSION STACK: \n' % self.__file_name)

        self.__benchmark = benchmark
        self.__log_data = log_data
        self.__image_width = matrix_data.shape[0]
        self.__image_height = matrix_data.shape[1]
        self.__original_data = matrix_data
        self.__compressed_data = self.__original_data
        self.__total_time = int()
        self.__encoding_table = None

    #endregion Constructors

    #region Public Functions

    def apply_simple_filter(self, up=True):

        """
        Function that applies Sub Filter (Delta Encoding) or Up Filter to the target data.
        :param up: flag that allows the usage of Up Filter instead of Sub filter (both filters are performed in the same function)
        :return:
        """

        if up:
            self.__log_file.write(' -> UP FILTER\n')
        else:
            self.__log_file.write(' -> SUB FILTER\n')

        now = time.perf_counter()

        if self.__benchmark:
            if up:
                print('Applying up filter...')
            else:
                print('Applying sub filter...')

        self.__compressed_data = sub.apply_simple_filter(self.__compressed_data, up=up)

        diff = time.perf_counter() - now
        self.__total_time += diff

        if self.__benchmark:
            if up:
                print('Ellapsed up filtering time: %.2f sec' % diff)
            else:
                print('Ellapsed sub filtering time: %.2f sec' % diff)

        if self.__log_data:
            print(self.__compressed_data)

    def apply_simplified_paeth_filter(self):

        """
        Function that applies the simplified version of Paeth filter to the target data.
        Example:
        B C         B - upper left pixel    P = A + C - B
        A X         C - above pixel         X' = X - P
                    A - previous pixel
                    X - current pixel
                    X' - filtered pixel
        :return:
        """

        self.__log_file.write(' -> SIMPLE PAETH FILTER\n')

        now = time.perf_counter()

        if self.__benchmark:
            print('Applying simple Paeth filter...')

        self.__compressed_data = paeth.apply_simplified_paeth_filter(self.__compressed_data, self.__image_width, self.__image_height)

        diff = time.perf_counter() - now
        self.__total_time += diff

        if self.__benchmark:
            print('Ellapsed simple Paeth filtering time: %.2f sec' % diff)

        if self.__log_data:
            print(self.__compressed_data)

    def apply_mtf(self):
        """
        Function that applies the Move To Front Transform (MTF) to the target data.
        Example:

        S = [1, 2, 3, 2, 3, 1]      A = [1, 2, 3]   S - target data
        S'= []                                      A - initial symbol list

        1. S' = [0]                     A = [1, 2, 3]
        2. S' = [0, 1]                  A = [2, 1, 3]
        3. S' = [0, 1, 2]               A = [3, 2, 1]
        4. S' = [0, 1, 2, 1]            A = [2, 3, 1]
        5. S' = [0, 1, 2, 1, 1]         A = [3, 2, 1]
        6. S' = [0, 1, 2, 1, 1, 2]      A = [1, 2, 3]

        :return:
        """
        self.__log_file.write(' -> MTF\n')

        now = time.perf_counter()

        if self.__benchmark:
            print('Applying MTF...')

        self.__compressed_data = np.array(mtf.apply_mtf(np.array(self.__compressed_data).ravel(), self.ALPHABET))

        diff = time.perf_counter() - now
        self.__total_time += diff

        if self.__benchmark:
            print('Ellapsed MTF encoding time: %.2f sec' % diff)

        if self.__log_data:
            print(self.__compressed_data)

    def apply_rle(self):
        """
        Function that applies Run-Length-Encoding (RLE) to the target data.
        Example:

        S = [1, 1, 1, 1, 1, 2, 3, 2, 2, 2, 2, 2]    S - target data
        E = -1                                      E - escape character
                                                    S' - encoded data
        S' = [-1, 1, 5, 2, 3, -1, 2, 5]

        :return:
        """
        self.__rle = True

        self.__log_file.write(' -> RLE\n')

        now = time.perf_counter()

        if self.__benchmark:
            print('Applying RLE encoding...')

        self.__compressed_data = np.array(rle.rle_encode(np.array(self.__compressed_data).ravel(), self.ESCAPE_CHARACTER)).astype(np.int32)

        diff = time.perf_counter() - now
        self.__total_time += diff

        if self.__benchmark:
            print('Ellapsed RLE encoding time: %.2f sec' % diff)

        if self.__log_data:
            print(self.__compressed_data)

    def apply_lzw(self, max_size, reset_dict):
        """
        Function that applies Lempel-Ziv-Whelch (LZW) to the target data (variation of LZ dictionary compression methods)
        :return:
        """
        self.__log_file.write(' -> LZW WITH DICT MAX SIZE OF %d' % max_size)

        if reset_dict:
            self.__log_file.write(' AND WITH DICT RESET\n')
        else:
            self.__log_file.write(' AND WITHOUT DICT RESET\n')

        now = time.perf_counter()

        if self.__benchmark:
            print('Applying LZW encoding...')

        self.__compressed_data = np.array(lzw.lzw_encode(self.__compressed_data, limit=max_size,
                                                         reset_dictionary=reset_dict))

        diff = time.perf_counter() - now
        self.__total_time += diff

        if self.__benchmark:
            print('Ellapsed LZW encoding time: %.2f sec' % diff)

        if self.__log_data:
            print(self.__compressed_data)

    def apply_lzma(self):
        """
            Function that applies Lempel-Ziv-Whelch (LZW) to the target data (variation of LZ dictionary compression methods).
            :return:
        """
        self.__log_file.write(' -> LZMA\n')

        now = time.perf_counter()

        if self.__benchmark:
            print('Applying LZMA encoding...')

        compressor = lzma.LZMACompressor(format=lzma.FORMAT_RAW, filters=[{'id':lzma.FILTER_LZMA2}])
        self.__compressed_data = compressor.compress(bytearray(np.array(self.__compressed_data))) + compressor.flush()

        diff = time.perf_counter() - now
        self.__total_time += diff

        if self.__benchmark:
            print('Ellapsed LZMA encoding time: %.2f sec' % diff)

        if self.__log_data:
            print(self.__compressed_data)

    def apply_huffman_encoding(self):
        """
            Function that applies Huffman Encoding to the target data (entropic encoder).
            :return:
        """
        self.__log_file.write(' -> HUFFMAN ENCODING\n')

        now = time.perf_counter()

        if self.__benchmark:
            print('Applying Huffman encoding...')

        self.__compressed_data = np.concatenate((self.__compressed_data, [self.EOF_SYMBOL]))
        self.__encoding_table = HuffmanCodec.from_data(self.__compressed_data).get_code_table()
        self.__compressed_data = frw.encode(self.__compressed_data, self.__encoding_table, eof_symbol=self.EOF_SYMBOL)

        diff = time.perf_counter() - now
        self.__total_time += diff

        if self.__benchmark:
            print('Ellapsed huffman encoding time: %.2f sec' % diff)

        if self.__log_data:
            print(self.__compressed_data)

    def write_in_file(self):
        output_file_name = self.__file_name.split('.')[0] + self.FILE_EXTENSION
        initial_size, compressed_size = os.path.getsize(self.__input_file_path), os.path.getsize(self.__output_file_path + output_file_name)
        compression_ratio = (initial_size - compressed_size) / initial_size * 100
        self.__log_file.write('\nTOTAL ELLAPSED COMPRESSION TIME: %.2f sec.\n'
                            'INITIAL IMAGE SIZE: %d bytes\n'
                            'COMPRESSED IMAGE SIZE: %d bytes\n'
                            'COMPRESSION RATIO: %.2f%%\n' % (self.__total_time, initial_size, compressed_size, compression_ratio))
        self.__log_file.close()
        if self.__benchmark:
            print('Total ellapsed compression time: %.2f sec' % self.__total_time)
            print('Writing in file %s...' % output_file_name)
        frw.write_file(self.__output_file_path + output_file_name, self.__compressed_data,
                       self.__build_cmp_header())

    def toggle_benchmark(self):
        self.__benchmark = not self.__benchmark

    def toggle_log_data(self):
        self.__log_data = not self.__log_data

    #endregion Getters

    #endregion Public Functions

    #region Private Functions

    def __build_cmp_header(self):
        header = {
                'size': self.__image_width * self.__image_height,
                'width': self.__image_width,
                'height': self.__image_height,
                'rle': self.__rle
            }
        if self.__encoding_table:
            header['encoding_table'] = self.__encoding_table
        return header

    #endregion Private Functions

"""
    Class that encapsulates the information about a custom .bmp decompressor. The functions applied must be in the same order as the one
    used while using BMPCompressor so the file is correctly decompressed.
"""


class CMPDecompressor:

    #region Constants

    EOF_SYMBOL = _EndOfFileSymbol()
    ESCAPE_CHARACTER = -256
    FILE_EXTENSION = '.bmp'
    ALPHABET = [i for i in range(256)]

    #endregion Constants

    #region Constructors

    def __init__(self, input_file_path, output_file_path, benchmark=False, log_data=False):

        if not input_file_path.endswith('cmp'):
            raise InvalidFileExtensionError

        self.__input_file_path = input_file_path
        self.__output_file_path = output_file_path

        self.__header, self.__compressed_data = frw.read_file(input_file_path)
        if log_data:
            print(self.__compressed_data)

        self.__benchmark = benchmark
        self.__log_data = log_data
        self.__total_time = int()
        self.__original_data = self.__compressed_data

    #endregion Constructors

    #region Public Functions

    def apply_inverse_huffman_encoding(self):
        if self.__benchmark:
            now = time.perf_counter()
            print('Applying Inverse Huffman Encoding...')
        self.__original_data = frw.decode(self.__original_data, self.__header['encoding_table'], self.EOF_SYMBOL)
        if self.__benchmark:
            diff = time.perf_counter() - now
            self.__total_time += diff
            print('Ellapsed huffman encoding inversion time: %.2f sec' % diff)
        if self.__log_data:
            print(self.__original_data)

    def apply_inverse_rle(self):
        if self.__benchmark:
            now = time.perf_counter()
            print('Applying Inverse RLE...')
        self.__original_data = np.array(rle.rle_decode(self.__original_data, self.ESCAPE_CHARACTER))
        if self.__benchmark:
            diff = time.perf_counter() - now
            self.__total_time += diff
            print('Ellapsed RLE inversion time: %.2f sec' % diff)
        if self.__log_data:
            print(self.__original_data)

    def apply_inverse_lzw(self):
        if self.__benchmark:
            now = time.perf_counter()
            print('Applying Inverse LZW Encoding ...')
        self.__original_data = np.array(lzw.lzw_decode(self.__original_data))
        if self.__benchmark:
            diff = time.perf_counter() - now
            self.__total_time += diff
            print('Ellapsed Inverse LZW Encoding time: %.2f sec' % diff)
        if self.__log_data:
            print(self.__original_data)

    def apply_inverse_lzma(self):
        if self.__benchmark:
            now = time.perf_counter()
            print('Applying Inverse LZMA Encoding ...')
        decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=[{'id':lzma.FILTER_LZMA2}])
        if self.__header['rle']:
            self.__original_data = np.frombuffer(decompressor.decompress(self.__original_data), dtype=np.int32)
        else:
            self.__original_data = np.frombuffer(decompressor.decompress(self.__original_data), dtype=np.uint8)
        if self.__benchmark:
            diff = time.perf_counter() - now
            self.__total_time += diff
            print('Ellapsed Inverse LZMA Encoding time: %.2f sec' % diff)
        if self.__log_data:
            print(self.__original_data)

    def apply_inverse_mtf(self):
        if self.__benchmark:
            now = time.perf_counter()
            print('Applying Inverse MTF...')
        self.__original_data = np.array(mtf.invert_mtf(self.__original_data, self.ALPHABET)).astype(np.uint8)
        if self.__benchmark:
            diff = time.perf_counter() - now
            self.__total_time += diff
            print('Ellapsed MTF inversion time: %.2f sec' % diff)
        if self.__log_data:
            print(self.__original_data)

    def apply_inverse_simple_filter(self, up):
        warnings.filterwarnings('ignore')
        if self.__benchmark:
            now = time.perf_counter()
            print('Applying inverse simple filter...')
        self.__original_data = sub.invert_simple_filter(self.__original_data, self.__header['width'], self.__header['height'], up=up)
        if self.__benchmark:
            diff = time.perf_counter() - now
            self.__total_time += diff
            print('Ellapsed simple filter inversion time: %.2f sec' % diff)
        if self.__log_data:
            print(self.__original_data)

    def apply_inverse_simplified_paeth_filter(self):
        if self.__benchmark:
            now = time.perf_counter()
            print('Applying inverse simple Paeth filter...')
        self.__original_data = paeth.invert_simplified_paeth_filter(self.__original_data, self.__header['width'], self.__header['height'])
        if self.__benchmark:
            diff = time.perf_counter() - now
            self.__total_time += diff
            print('Ellapsed inverse simple Paeth filtering time: %.2f sec' % diff)
        if self.__log_data:
            print(self.__original_data)

    def write_in_file(self, show_image=False):
        output_file_name = self.__input_file_path.split('/')[::-1][0].split('.')[0] + self.FILE_EXTENSION
        self.__original_data = np.reshape(np.array(self.__original_data).astype(np.uint8), (self.__header['width'], self.__header['height']))
        image = Image.fromarray(self.__original_data, 'L')
        if show_image:
            Image._show(image)
        if self.__benchmark:
            print('Writing in file %s...' % output_file_name)
        image.save(self.__output_file_path + output_file_name)

    def toggle_benchmark(self):
        self.__benchmark = not self.__benchmark

    def toggle_log_data(self):
        self.__log_data = not self.__log_data

    #endregion Public Functions
