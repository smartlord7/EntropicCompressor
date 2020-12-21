from source_code.cmp.modules.filters import subup as subup
import numpy as np

"""
Driver program for testing purposes - Sub/Up Filter
"""
def main():
    if __name__ == '__main__':
        data = np.array([np.array([1, 2, 3]),
                        np.array([1, 2, 3]),
                        np.array([2, 1, 3]),
                        np.array([3, 2, 1]),
                        np.array([1, 2, 2]),
                        np.array([255, 0, 255])], dtype=np.uint8)
        encoded = subup.apply_simple_filter(data, up=False)
        print(encoded)
        decoded = subup.invert_simple_filter(encoded, 6, 3, up=False)
        print(decoded)

main()