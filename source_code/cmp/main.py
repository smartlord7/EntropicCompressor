from source_code.cmp.Codec import BMPCompressor, CMPDecompressor
import warnings
import os

TO_COMPRESS_PATH = '../../resources/images/uncompressed/original/'
COMPRESSED_PATH = '../../resources/images/compressed/generations/13/'
UNCOMPRESSED_PATH = '../../resources/images/uncompressed/from_cmp/'


def compress_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp'):
                print('\n-------------------- \n%s Compression\n--------------------' % file)
                comp = BMPCompressor(TO_COMPRESS_PATH + file, COMPRESSED_PATH, benchmark=True)
                #comp.apply_simple_filter(True)
                comp.apply_simplified_paeth_filter()
                #comp.apply_rle()
                #comp.apply_huffman_encoding()
                comp.apply_lzma()
                #comp.apply_lzw(16384, False)
                comp.write_in_file()
                print('--------------------')


def uncompress_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.cmp'):
                print('\n-------------------- \n%s Decompression\n--------------------' % file)
                decomp = CMPDecompressor(COMPRESSED_PATH + file, UNCOMPRESSED_PATH)
                decomp.apply_inverse_lzma()
                #decomp.apply_inverse_huffman_encoding()
                #decomp.apply_inverse_rle()
                #decomp.apply_inverse_lzw()
                decomp.apply_inverse_simplified_paeth_filter()
                #decomp.apply_inverse_simple_filter(True)
                decomp.write_in_file(show_image=True)


def main():
    if __name__ == '__main__':
        warnings.filterwarnings('ignore')
        compress_files(TO_COMPRESS_PATH)
        uncompress_files(COMPRESSED_PATH)

main()