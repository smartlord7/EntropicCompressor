"""------------CODEC's nao destrutivos para imagens monocromaticas------------
Universidade de Coimbra
Licenciatura em Engenharia Informatica
Teoria da Informacao
Segundo ano, primeiro semestre

Authors:
João Afonso Vieira de Sousa, 2019224599, uc2019224599@student.uc.pt
José Domingos da Silva, 2018296125, uc2018296125@student.uc.pt
Sancho Amaral Simões, 2019217590, uc2019217590@student.uc.pt
Tiago Filipe Santa Ventura, 2019243695, uc2019243695@student.uc.pt

19/12/2020
---------------------------------------------------------------------------"""

#region Public Functions


def rle_encode(data, escape_character=-256):
    """
    Function that RLE encodes a given piece of data.
    :param data: the target data.
    :param escape_character: the character that is used to indicate that a run of symbols has been compressed.
    :return: the RLE encoded data.
    """
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
    """
    Function that RLE decodes a given piece of data.
    :param encoded_data: the target data.
    :param escape_character: the character that is used to indicate that a run of symbols has been compressed.
    :return: the RLE decoded data.
    """
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


#endregion Public Functions