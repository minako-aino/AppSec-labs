import os
from arc4 import ARC4
import pandas as pd
import numpy as np


def get_key():
    mk = open('master.key')
    key = bytes(mk.read().encode('utf-8').strip())
    mk.close()

    return key


def decrypt(data):
    key = get_key()

    arc4 = ARC4(key)

    for col in data.columns:
        for row in range(0, data.shape[0]):
            plaintext = arc4.decrypt(data[col][row]).decode('utf-8', 'ignore')
            data[col][row] = plaintext
    return data


def encrypt(data):
    # key
    key = get_key()

    # add some randomness
    nonce = os.urandom(4).decode('utf-8', 'replace')
    tempkey = (key+bytes(nonce, encoding='utf8'))
    arc4 = ARC4(tempkey)

    # change the dataset
    data = pd.DataFrame(np.zeros(shape=(data.shape[0], data.shape[1])), columns=data.columns)
    for col in data.columns:
        for row in range(0, data.shape[0]):
            data[col][row] = arc4.encrypt(str(data[col][row]))

    data.to_csv('vault.csv')
    return data, tempkey
