from source_code.cmp.Codec import BMPCompressor, CMPDecompressor
import os

TO_COMPRESS_PATH = '../../resources/images/uncompressed/original/'
TO_UNCOMPRESS_PATH = '../../resources/images/compressed/generations/2/'
UNCOMPRESSED_PATH = '../../resources/images/uncompressed/generations/2/'


def compress_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp'):
                print('\n---------- \n%s Compression\n----------' % file)
                comp = BMPCompressor(TO_COMPRESS_PATH + file, TO_UNCOMPRESS_PATH, log=True)
                comp.apply_simple_filter(True)
                comp.apply_lzw()
                comp.apply_huffman_encoding()
                comp.write_in_file()
                print('----------')


def uncompress_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.cmp'):
                print('\n---------- \n%s Decompression\n----------' % file)
                decomp = CMPDecompressor(TO_UNCOMPRESS_PATH + file, UNCOMPRESSED_PATH, log=True)
                decomp.apply_inverse_huffman_encoding()
                decomp.apply_inverse_lzw()
                decomp.apply_inverse_simple_filter(True)
                decomp.write_in_file(show_image=True)


def main():
    if __name__ == '__main__':
        compress_files(TO_COMPRESS_PATH)
        uncompress_files(TO_UNCOMPRESS_PATH)

main()