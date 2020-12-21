import source_code.cmp.modules.filters.util as util
import numpy as np


def apply_simple_filter(data, up=False):
    data = util.to_numpy_uint8(data)
    if up:
        data = np.transpose(data)
    data = data.ravel()
    return np.concatenate(([data[0]], np.diff(data)))


def invert_simple_filter(data, width, height, up=False):
    data = np.cumsum(data).astype(np.uint8)
    if up:
        return np.transpose(data.reshape((height, width)))
    return data.reshape((width, height))

def main():
    if __name__ == '__main__':
        data = np.array([np.array([1, 2, 3]),
                        np.array([1, 2, 3]),
                        np.array([2, 1, 3]),
                        np.array([3, 2, 1]),
                        np.array([1, 2, 2]),
                        np.array([255, 0, 255])], dtype=np.uint8)
        encoded = apply_simple_filter(data, up=False)
        print(encoded)
        decoded = invert_simple_filter(encoded, 6, 3, up=False)
        print(decoded)

main()