# Bit stream encoding demo
# Developed by Marco Simões on 07/12/2020
# msimoes@dei.uc.pt
"""------------CODEC's nao destrutivos para imagens monocromaticas------------
Universidade de Coimbra
Licenciatura em Engenharia Informatica
Teoria da Informacao
Segundo ano, primeiro semestre

Coauthors (edited):
João Afonso Vieira de Sousa, 2019224599, uc2019224599@student.uc.pt
José Domingos da Silva, 2018296125, uc2018296125@student.uc.pt
Sancho Amaral Simões, 2019217590, uc2019217590@student.uc.pt
Tiago Filipe Santa Ventura, 2019243695, uc2019243695@student.uc.pt

19/12/2020
---------------------------------------------------------------------------"""

import pickle

#region Public Functions


def encode(data, table, eof_symbol):
    """
    Function that encodes the specified piece of data in a bytearray, ensuring that occupies the least space possible.
    :param data: the data to be encoded.
    :param table: the encoding table from which the codes and their lengths will be extracted.
    :param eof_symbol: the symbol that indicates the end of the data stream.
    :return: the bytearray correspondent to the given data.
    """
    encoded_data = bytearray()

    data = list(data) + [eof_symbol]

    buffer = 0
    size = 0
    for s in data:

        # vou buscar o codigo binario para codificar o simbolo s
        # b -> "comprimento" (num de bits) do cdigo, v -> valor do codigo
        b, v = table[s]
       
        # vou adicionar o codigo binario ao buffer. Para isso faço:
        # Shift left do comprimento do simbolo a adicionar e adição do respetivo valor.
        # Exemplo: buffer tem valor 101, e vou adicionar o valor 10
        # 1) shift left de duas casa (buffer << 2) -> 10100
        # 2) somar o simbolo ao buffer ( buffer + 10 ) -> 10110
        buffer = (buffer << b) + v

        size += b
        # aumento a contagem de bits do buffer

        # se ja tenho bits para retirar um byte completo
        while size >= 8:
            
            # shift right de tudo menos os 8 primeiros bits
            # Exemplo: 1000101010 >> (10-8) -> 10001010
            byte = buffer >> (size - 8)
            
            # adicionar o byte ao array de bytes codificados
            encoded_data.append( byte )

            # remover byte do buffer. 
            # Para isso vou pegar no byte e fazer um shift left de (size - 8) e subtrai-lo o buffer
            # 100010 << (10-8) -> 10001000
            # 10001010 (buffer) - 10001000 -> 10
            buffer = buffer - (byte << (size - 8))
            size -= 8
        
    # se houverem bits no buffer depois de codificar toda a fonte
    if size > 0:
        byte = buffer << (8 - size)
        encoded_data.append( byte )
    

    return encoded_data


def decode(encoded_data, table, eof_symbol):
    """
    Function that converts a stream of a bytes of a compressed data source into a list, given its encoding table.
    :param encoded_data: the data to be decoded.
    :param table: the encoding table.
    :param eof_symbol: the symbol that indicates the end of the byte stream.
    :return: the decoded data as a list.
    """
    decoded_data = []

    # inverte tabela: mapeia (bitsize, value) para symbols
    lookup = {(b, v): s for s, (b, v) in table.items()}

    # mascaras para tirar apenas um bit do byte, do mais significativo para o menos
    masks = [     128,      64,      32,      16,       8,       4,       2,       1]
    #        10000000 01000000 00100000 00010000 00001000 00000100 00000010 00000001


    buffer = 0
    size = 0
    counter = 0
    # vou percorrer os bytes codificados
    for byte in encoded_data:
        # vou tirar bit a bit, do mais significativo para o menos, e juntando ao buffer
        for m in masks:
            buffer = (buffer << 1) + bool(byte & m)
            size += 1

            # se o buffer de bits e o tamanho existirem na tabela, retiro esse simbolo!
            if (size, buffer) in lookup:
                symbol = lookup[size, buffer]

                if symbol == eof_symbol:
                    return decoded_data
                
                decoded_data.append(symbol)

                # reinicio o buffer                
                buffer = 0
                size = 0
        counter += 1


def write_file(filename, data, header):
    """
    Function that serializes the compressed image data and its header to a binary file.
    :param filename: the target file's name.
    :param data: the compressed image data.
    :param header: the data's header.
    :return:
    """
    if type(header) == dict:
        with open(filename, 'wb') as f:
            pickle.dump(header, f)
            pickle.dump(data, f)
            f.close()


def read_file(filename):
    """
    Function that deserializes the compressed image data and its header from a binary file.
    :param filename: the target file's name.
    :return: the read data and its header.
    """
    with open(filename, 'rb') as f:
        header = pickle.load(f)
        data = pickle.load(f)
        f.close()
        return header, data


#endregion Public Functions


