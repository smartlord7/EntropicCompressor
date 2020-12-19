import time


def apply_mtf(data, alphabet):
    encoded, symbol_list = list(), alphabet[::]
    counter = int()
    for char in data:
        index = symbol_list.index(char)
        encoded.append(index)
        symbol_list = [symbol_list.pop(index)] + symbol_list
        counter += 1
    return encoded


def invert_mtf(data, alphabet):
    decoded, symbol_list = list(), alphabet[::]
    for index in data:
        symbol = symbol_list[index]
        decoded.append(symbol)
        symbol_list = [symbol_list.pop(index)] + symbol_list
    return decoded


def main():
    if __name__ == '__main__':
        now = time.perf_counter()
        alphabet = [0, 1, 2, 3]
        string = [1, 3, 2, 1, 0]
        encoded = apply_mtf(string, alphabet)
        print(encoded)
        decoded = invert_mtf(encoded, alphabet)
        print(decoded)
        print(string == decoded)
        print(time.perf_counter() - now)
main()