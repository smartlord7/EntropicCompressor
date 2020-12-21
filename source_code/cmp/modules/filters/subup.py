import source_code.cmp.modules.filters.util as util
import numpy as np


def apply_simple_filter(data, up=False):
    """
    Function that applies Sub/Up Filter in a given piece of data.
    :param data: the data to be filtered.
    :param up: flag that indicates if the Up Filter must be used instead of the Sub Filter.
    :return: the filtered data.
    """
    data = util.to_numpy_uint8(data)
    if up:
        data = np.transpose(data)
    data = data.ravel()
    return np.concatenate(([data[0]], np.diff(data)))


def invert_simple_filter(data, width, height, up=False):
    """
    Function that applies Inverse Sub/Up Filter in a given piece of data.
    :param data: the data to be unfiltered.
    :param up: flag that indicates if the Up Filter was used instead of the Sub Filter.
    :return: the unfiltered data.
    """
    data = np.cumsum(data).astype(np.uint8)
    if up:
        return np.transpose(data.reshape((height, width)))
    return data.reshape((width, height))