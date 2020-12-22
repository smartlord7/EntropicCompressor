"""------------CODEC's nao destrutivos para imagens monocromaticas------------
Universidade de Coimbra
Licenciatura em Engenharia Informatica
Teoria da Informacao
Segundo ano, primeiro semestre

Authors:
João Afonso Vieira de Sousa, 2019224599, uc2019224599@student.uc.pt
José Domingos da Silva, 2018296125, uc2018296125@student.uc.pt
Sancho Amaral Simões, 2019217590, uc2019217590@student.uc.pt
Tiago Filipe Santa Ventura, 2019243695, uc2019243695@student.uc.pt

19/12/2020
---------------------------------------------------------------------------"""

from source_code.cmp.CMPCodec import CMPCompressor, CMPDecompressor
import warnings
import os

#region Constants

TO_COMPRESS_PATH = '../../resources/images/uncompressed/original/'
COMPRESSED_PATH = '../../resources/images/compressed/generations/1/'
TO_DECOMPRESS_PATH = '../../resources/images/compressed/generations/1/'
DECOMPRESSED_PATH = '../../resources/images/uncompressed/from_cmp/'

#endregion Constants

#region Public Functions


def compress_files(files_dir):
    """
    Given a directory, this function loops through all the .bmp images inside it and applies the specified algorithms below in order
    to compress the files in question.
    :param files_dir: the directory in which the target .bmp files are.
    :return:
    """
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.bmp'):
                print('\n-------------------- \n%s Compression\n--------------------' % file)
                comp = CMPCompressor(TO_COMPRESS_PATH + file, COMPRESSED_PATH, benchmark=True)
                comp.apply_simple_filter(True)
                #comp.apply_simplified_paeth_filter()
                #comp.apply_mtf()
                comp.apply_rle()
                comp.apply_huffman_encoding()
                #comp.apply_lzw(1024, False)
                #comp.apply_huffman_encoding()
                comp.write_in_file()
                comp.output_log()
                print('--------------------')


def decompress_files(files_dir):
    """
       Given a directory, this function loops through all the .cmp files inside it and applies the specified algorithms below in order
       to decompress the files in question.
       :param files_dir: the directory in which the target .cmp files are.
       :return:
    """
    for subdir, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith('.cmp'):
                print('\n-------------------- \n%s Decompression\n--------------------' % file)
                decomp = CMPDecompressor(COMPRESSED_PATH + file, DECOMPRESSED_PATH, benchmark=True)
                #decomp.apply_inverse_lzma()
                decomp.apply_inverse_huffman_encoding()
                decomp.apply_inverse_rle()
                #decomp.apply_inverse_lzw()
                #decomp.apply_inverse_simplified_paeth_filter()
                #decomp.apply_inverse_mtf()
                decomp.apply_inverse_simple_filter(True)
                decomp.write_in_file(show_image=True)
                decomp.output_log()
                print('--------------------')


def main():
    """
    Driver program - CMP Codec Test
    """
    if __name__ == '__main__':
        warnings.filterwarnings('ignore')
        compress_files(TO_COMPRESS_PATH)
        decompress_files(TO_DECOMPRESS_PATH)


#endregion Public Functions


main()