# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 11:45:53 2020

@author: José Silva
"""
import matplotlib.image as img

import numpy as np
from typing import List, Tuple, Union
# Instead of always transmitting an "original" dictionary, it is simpler to just agree on an initial set.
# Here we use the 256 possible values of a byte:
common_dictionary = list(range(256))

def encode(a):
    # Change to bytes for 256.

    # Changing the common dictionary is a bad idea. Make a copy.
    dictionary = common_dictionary.copy()

    # Transformation
    compressed_text = list()          # Regular array
    rank = 0

    # Read in each character
    for c in a:
        rank = dictionary.index(c)    # Find the rank of the character in the dictionary [O(k)]
        compressed_text.append(rank)  # Update the encoded text

        # Update the dictionary [O(k)]
        dictionary.pop(rank)
        dictionary.insert(0, c)

    return compressed_text            # Return the encoded text

def decode(a):
    compressed_text = a
    dictionary = common_dictionary.copy()
    plain_text = []

    # Read in each rank in the encoded text
    for rank in compressed_text:
        # Read the character of that rank from the dictionary
        plain_text.append(dictionary[rank])

        # Update the dictionary
        e = dictionary.pop(rank)
        dictionary.insert(0, e)

    return plain_text  # Return original string
    
    
f=img.imread("../resources/images/uncompressed_images/egg.bmp")
f=f[:5,:5]
f=f.flatten()
print(f)
f=encode(f)
print(f)
f=decode(f)
print(f)
