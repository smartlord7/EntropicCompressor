from source_code.cmp.modules.filters import util as util


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
        util.show_progress(counter, len(data))
        index = symbol_list.index(char)
        encoded.append(index)
        symbol_list = [symbol_list.pop(index)] + symbol_list
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
    for index in data:
        symbol = symbol_list[index]
        decoded.append(symbol)
        symbol_list = [symbol_list.pop(index)] + symbol_list
    return decoded