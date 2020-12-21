from source_code.cmp.modules.filters import paeth
import numpy as np

"""
Driver program - for testing purposes - Simplified Paeth filter
"""
def main():
    if __name__ == '__main__':
        width, height = 10, 10
        data = np.random.randint(0, 10, (width, height))
        encoded = paeth.apply_simplified_paeth_filter(data, width, height)
        print('Encoded')
        print(encoded)
        decoded = paeth.invert_simplified_paeth_filter(encoded, width, height)
        print('Decoded')
        print(decoded == data)
        #print(__get_left_mattrix(data))
        #print(__get_above_mattrix(data))
        #print(__get_upper_left_mattrix(data))

main()