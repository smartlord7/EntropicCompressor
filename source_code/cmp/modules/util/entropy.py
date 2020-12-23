import numpy as np
import matplotlib.pyplot as plt

#region Public Functions


def gen_alphabet(data):
    """
        Function that calculates the alphabet from a given numpy array.
        :param data: the data from which the alphabet will me be generated.
        :return: the data's alphabet:
            -if it is an array of strings, it will return
                a numpy array array containing the upper and lowercase characters of the english alphabet
            -if it is a numeric array, it will return
                a numpy array ranging from zero to 2 powered to the number of bits required to encode that type of number
    """
    assert(type(data) == np.ndarray)
    if type(data[0]) == np.str_:
        alphabet = [chr(ord('A') + i) if i <= 25 else chr((ord('a') + (i % 26))) for i in range(52)]
    else:
        amplitude = 2 ** get_num_quantization_bits(data)
        alphabet = np.arange(0, amplitude)
    return alphabet


def gen_histogram(data, alphabet_length=0):
    """
        Function that generates a histogram of occurrences of a certain array.
        The order of the symbols is the same as in the function gen_alphabet.
        :param data: the data from which the histogram will be generated.
        :param alphabet_length: optional parameter that specifies the length of the alphabet. Only used
            if the data array is numeric.
        :return: the data' histogram (numpy array).
    """
    if type(data[0]) == np.str_:
        histogram = np.zeros(52)
        for i in range(0, len(data)):
            current = data[i]
            if 'A' <= current <= 'Z':
                histogram[ord(current) - ord('A')] += 1
            elif 'a' <= current <= 'z':
                histogram[ord(current) - ord('a') + 26] += 1
    else:
        histogram = np.zeros(alphabet_length)
        for value in data:
            histogram[value] += 1
    return histogram


def plot_histogram(alphabet, histogram, title, ticks_size=5):
    """
        Function that plots the histogram of occurrences of a certain piece of data.
        :param alphabet: the data's alphabet. It will be showed in x-axis.
        :param histogram: the data's histogram.
        :param title: the plot's title.
        :param ticks_size: optional param that specifies the size of the ticks in x-axis.
    """
    plt.xticks(fontsize=ticks_size)
    plt.bar(alphabet, histogram)
    plt.title(title)
    plt.ylabel('Number of occurrences')
    plt.xlabel('Symbol')
    plt.show()


def get_num_quantization_bits(data):
    """
        Function that retrieves the number of quantization bits used in encoding a certain numeric type in a numpy array.
        :param data: the data from which the number of quantization bits will be extracted (numpy array).
        :return: the number of quantization bits used in encoding a certain numeric type in the data array.
    """
    assert(type(data) == np.ndarray and data.dtype != np.str_)
    num_bits = str()
    dtype = str(data.dtype)
    for char in dtype:
        if char.isdigit():
            num_bits += char
    return int(num_bits)


def entropy(histogram, length):
    """
        Function that calculates the entropy of a certain piece of data, given its histogram.
        :param histogram: the data's histogram (numpy array).
        :param length: the data's length.
        :return: the data's entropy.
    """
    assert(type(histogram) == np.ndarray)
    probabilities = histogram[histogram > 0] / length
    return -np.sum(probabilities * np.log2(probabilities))


def gen_histogram_generic(data, group_size=1):
    """
        Function that, given data and assuming groups of group_size symbols, generates its histogram.
        :param data: the data from which the histogram will be generated.
        :param group_size: the size of each group of symbols.
        :return: a dictionary that corresponds to the data's histogram.
    """
    if type(data) != np.ndarray:
        data = np.array(list(data))
    histogram = dict()
    length = len(data)
    num_groups = int(length / group_size)
    for i in range(num_groups):
        current_index = group_size * i
        current_group = str()
        for j in range(group_size):
            current_group += str(data[current_index + j])
            if j < group_size - 1:
                current_group += "."
        histogram.setdefault(current_group, 0)
        histogram[current_group] += 1
    return histogram, num_groups


def entropy_generic(histogram, num_groups, group_size):
    """
        Function that calculates the entropy of a certain piece of data, assuming groups of group_size symbols.
        :param histogram: the data's histogram (dictionary).
        :param num_groups: the number of groups of group_size symbols that fit in the data.
        :param group_size: the size of each group of symbols.
        :return: the data's entropy.
    """
    assert(type(histogram) == dict)
    probabilities = np.array([value for value in histogram.values()]) / num_groups
    return -np.sum(probabilities * np.log2(probabilities)) / group_size


def plot_histogram_generic(histogram, title, display_keys=True, ticks_size=5):
    """
        Function that plots the histogram of occurrences of a certain piece of data.
        :param histogram: the data's histogram.
        :param title: the plot's title.
        :param display_keys: optional param:
            if true: the histogram (dictionary) keys are displayed as keys in the plot
            else: the histogram keys (dictionary) are are displayed as keys in the plot
        :param ticks_size: optional param that specifies the size of the ticks in x-axis.
    """
    sorted_hist = [(key, histogram[key]) for key in sorted(histogram)]
    if display_keys:
        keys = [tup[0] for tup in sorted_hist]
    else:
        keys = [x for x in range(len(histogram))]
    values = [tup[1] for tup in sorted_hist]
    plt.xticks(fontsize=ticks_size)
    plt.title(title)
    plt.bar(keys, values)
    plt.show()


#endregion Public Functions