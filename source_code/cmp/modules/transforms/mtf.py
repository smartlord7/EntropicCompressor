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

from source_code.cmp.modules.filters import util as util

#region Public Functions


def apply_mtf(data, alphabet):
    """
    Function that applies the Move To Front Transform on a given piece of data.
    :param data: the target data.
    :param alphabet: the data's alphabet.
    :return: the MTF encoded data.
    """
    encoded, symbol_list = list(), alphabet[::]
    counter = int()
    for char in data:
        #util.show_progress(counter, len(data))
        index = symbol_list.index(char)
        encoded.append(index)
        symbol_list.pop(index)
        symbol_list.insert(0, char)
        counter += 1
    return encoded


def invert_mtf(data, alphabet):
    """
    Function that applies the Inverse Move To Front Transform on a given piece of data.
    :param data: the target data to be decoded.
    :param alphabet: the data's alphabet.
    :return: the MTF decoded data.
    """
    decoded, symbol_list = list(), alphabet[::]
    counter = int()
    for index in data:
        #util.show_progress(counter, len(data))
        symbol = symbol_list[index]
        decoded.append(symbol)
        symbol_list = [symbol_list.pop(index)] + symbol_list
        counter += 1
    return decoded


#endregion Public Functions