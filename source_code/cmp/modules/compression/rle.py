

def rle_encode(data, escape_character=-256):
    encoded_data = list()
    length = len(data)
    i = int()
    while i < length:
        if i == length - 1:
            encoded_data.append(data[i])
            break
        current = data[i]
        nextIndex = i + 1
        next = data[nextIndex]
        while current == next:
            nextIndex += 1
            if nextIndex >= length:
                break
            next = data[nextIndex]
        if nextIndex - i > 3:
            encoded_data.append(escape_character)
            encoded_data.append(current)
            encoded_data.append(nextIndex - i)
        else:
            for i in range(nextIndex - i):
                encoded_data.append(current)
        i = nextIndex
    return encoded_data



def rle_decode(encoded_data, escape_character=-256):
    decoded_data = list()
    length = len(encoded_data)
    i = int()
    while i < length:
        current = encoded_data[i]
        if current == escape_character:
            character = encoded_data[i + 1]
            times = encoded_data[i + 2]
            for j in range(times):
                decoded_data.append(character)
            i += 3
        else:
            decoded_data.append(current)
            i += 1
    return decoded_data