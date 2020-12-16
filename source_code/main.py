from source_code.Codec import BMPCompressor, CMPDecompressor
import os
import warnings


TO_COMPRESS_PATH = '../resources/images/uncompressed/'
TO_UNCOMPRESS_PATH = '../resources/images/compressed/generations/generation1/'


def compress_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp'):
                print('\n---------- \n%s Compression\n----------' % file)
                comp = BMPCompressor(TO_COMPRESS_PATH + file, TO_UNCOMPRESS_PATH, log=True)
                print(comp.get_flattened_data()[:200])
                comp.all_compress()
                comp.write_in_file()
                print('----------')


def uncompress_files(files_dir):
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.cmp'):
                print('\n---------- \n%s Uncompression\n----------' % file)
                decomp = CMPDecompressor(TO_UNCOMPRESS_PATH + file, '', log=True)
                decomp.all_uncompress()
                print(decomp.get_original_data()[:200])



def main():
    if __name__ == '__main__':
        #compress_files(TO_COMPRESS_PATH)
        uncompress_files(TO_UNCOMPRESS_PATH)

main()