from source_code.cmp.modules.transforms import mtf

"""
Driver program for testing purposes - Move To Front Transform
"""
def main():
    if __name__ == '__main__':
        alphabet = [0, 1, 2, 3]
        string = [1, 3, 2, 1, 0]
        encoded = mtf.apply_mtf(string, alphabet)
        print(encoded)
        decoded = mtf.invert_mtf(encoded, alphabet)
        print(decoded)
        print(string == decoded)
main()