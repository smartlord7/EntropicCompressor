import numpy as np


def to_numpy_uint8(data):
    if type(data) != np.ndarray:
        data = np.array(data).astype(np.uint8)
    return data


def show_progress(counter, length):
    if not counter % 100000:
        print('%.2f%%' % (counter / length * 100))