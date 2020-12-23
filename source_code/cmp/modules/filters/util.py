import numpy as np


def to_numpy_uint8(data):
    """
    Util function that converts an iterable to a numpy uint8 array.
    :param data: the iterable to be converted.
    :return: the converted iterable.
    """
    if type(data) != np.ndarray:
        data = np.array(data).astype(np.uint8)
    return data


def show_progress(counter, length):
    """
        Util function that shows in the console the current progress, in percentage, of
        the algorithm that is being applied on the data in question.
        :param counter: the current index in the data.
        :param length: the data's length.
        :return:
    """
    if not counter % 100000:
        print('%.2f%%' % (counter / length * 100))