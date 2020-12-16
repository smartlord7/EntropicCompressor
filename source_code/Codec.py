import source_code.modules.filters.filters as filt
import source_code.modules.compression.rle as rle
import lib.encoding_file_writer as frw
import matplotlib.image as img
import warnings
import time
from lib.huffmancodec import HuffmanCodec, _EndOfFileSymbol


class InvalidFileExtensionError(Exception):
    pass


class InvalidImageColorSpaceError(Exception):
    pass


class BMPCompressor:

    INITIAL_ALPHABET_LENGTH = 256
    ESCAPE_CHARACTER = -256
    EOF_SYMBOL = _EndOfFileSymbol()
    FILE_EXTENSION = '.cmp'

    def __init__(self, input_file_path, output_file_path, log=False):
        if not input_file_path.endswith('bmp'):
            raise InvalidFileExtensionError
        
        matrix_data = img.imread(input_file_path)
        if len(matrix_data.shape) != 2:
            raise InvalidImageColorSpaceError
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.log = log
        self.image_width = matrix_data.shape[0]
        self.image_height = matrix_data.shape[1]
        self.flattened_data = matrix_data.flatten()
        self.filtered_data = None
        self.transformed_data = None
        self.encoding_table = None
        self.compressed_data = None

    def apply_filters(self):
        if self.log:
            print('Filtering image...'
                  '\nApplying sub filter...')
        now = time.perf_counter()

        self.filtered_data = filt.apply_subtraction_filter(self.flattened_data)
        if self.log:
            print('Ellapsed filtering time: %.2f sec' % (time.perf_counter() - now))

    def apply_transformations(self):
        pass

    def apply_compression(self):
        now = time.perf_counter()
        if self.log:
            print('Applying RLE encoding...')
        if self.filtered_data.any():
            data = rle.rle_encode(self.filtered_data, self.ESCAPE_CHARACTER)
        else:
            data = rle.rle_encode(self.flattened_data, self.ESCAPE_CHARACTER)
        data.append(self.EOF_SYMBOL)
        if self.log:
            print('Applying Huffman encoding...')
        self.encoding_table = HuffmanCodec.from_data(data).get_code_table()
        self.compressed_data = frw.encode(data,  self.encoding_table, eof_symbol=self.EOF_SYMBOL)
        if self.log:
            print('Ellapsed compression time: %.2f sec' % (time.perf_counter() - now))

    def build_cmp_header(self):
        return {
            'width': self.image_width,
            'height': self.image_height,
            'encoding_table': self.encoding_table
        }

    def write_in_file(self):
        output_file_name = str()
        if self.log:
            output_file_name = self.input_file_path.split('/')[::-1][0].split('.')[0] + '.cmp'
            print(output_file_name)
            print('Writing in file: %s' % output_file_name)
        if self.compressed_data:
            frw.write_file(self.output_file_path + output_file_name, self.compressed_data,
                           self.build_cmp_header())

    def all_compress(self):
        if self.log:
            print('Compressing image...')
        now = time.perf_counter()
        self.apply_filters()
        self.apply_transformations()
        self.apply_compression()
        if self.log:
            print('Total ellapsed compression time: %.2f' % (time.perf_counter() - now))

    def toggle_log(self):
        self.log = not self.log

    def get_flattened_data(self):
        return self.flattened_data
    
    def get_filtered_data(self):
        return self.filtered_data
    
    def get_transformed_data(self):
        return self.transformed_data
    
    def get_compressed_data(self):
        return self.compressed_data
    

class CMPDecompressor:

    EOF_SYMBOL = _EndOfFileSymbol()
    ESCAPE_CHARACTER = -256
    FILE_EXTENSION = '.bmp'

    def __init__(self, input_file_path, output_file_path, log=False):
        warnings.filterwarnings('ignore')
        if not input_file_path.endswith('cmp'):
            raise InvalidFileExtensionError

        self.header, self.compressed_data = frw.read_file(input_file_path)
        self.log = log
        self.filtered_data = None
        self.original_data = None

    def apply_uncompression(self):
        now = time.perf_counter()
        if self.log:
            print('Applying Inverse Huffman Encoding...')
        data = frw.decode(self.compressed_data, self.header['encoding_table'], self.EOF_SYMBOL)
        if self.log:
            print('Applying Inverse RLE...')
        self.filtered_data = rle.rle_decode(data, self.ESCAPE_CHARACTER)
        if self.log:
            print('Ellapsed uncompression time: %.2f' % (time.perf_counter() - now))

    def apply_unfilter(self):
        now = time.perf_counter()
        if self.log:
            print('Unfiltering image...')
        self.original_data = filt.decode_subtraction_filter(self.filtered_data)
        if self.log:
            print('Ellapsed unfiltering time: %.2f' % (time.perf_counter() - now))

    def all_uncompress(self):
        now = time.perf_counter()
        self.apply_uncompression()
        self.apply_unfilter()
        if self.log:
            print('Total ellapsed uncompression time: %.2f' % (time.perf_counter() - now))

    def toggle_log(self):
        self.log = not self.log

    def get_compressed_data(self):
        return self.compressed_data

    def get_filtered_data(self):
        return self.filtered_data

    def get_original_data(self):
        return self.original_data









