import cv2
import numpy as np
import random

def str2bitseq(s, width=8):
    '''
    Input: s: character string
    Output: bit array in np.uint8
    '''
    binstr = ''.join([(bin(c).replace('0b', '')).zfill(width) for c in s.encode(encoding="utf-8")])
    bitseq = [np.uint8(c) for c in binstr]

    return bitseq


def bitseq2str(msgbits):
    '''
    Input: bit array in np.uint8
    Output: s: character string
    '''
    binstr = ''.join([bin(b & 1).strip('0b').zfill(1) for b in msgbits])
    str = np.zeros(np.int(len(msgbits) / 8)).astype(np.int)
    for i in range(0, len(str)):
        str[i] = int('0b' + binstr[(8 * i):(8 * (i + 1))], 2)

    return bytes(str.astype(np.int8)).decode()


def getBit(num, bit_idx):
    ''' From num, get the given bit specified by bit_idx
    '''
    return (num & (1 << (8 - bit_idx))) >> (8 - bit_idx)


def dct_embed(img_gray, msg, seed=2020):
    "An illustration of how data are embedded in pair-wise DCT coefficients,"
    " img_gray - of grayscale"
    " msg - the to be embedded msg composed of 0 and 1 only"
    " seed - the encryption password"

    if len(img_gray.shape) > 2:
        print("Parameter img should be of grayscale")
        return img_gray

    # Step 1: check embedding capacity
    msg2embed = str2bitseq(msg)
    len_msg = len(msg2embed)
    # print(len_msg, msg2embed)

    # EC: embedding capacity
    # 1 bit is hided in each N by N block
    N = 8
    height, width = img_gray.shape
    EC = np.int((height) * (width) / N / N)
    if EC < len_msg:
        print('Embedding Capacity {} not enough'.format(EC))
        return img_gray

    # encrypted msg2embed
    random.seed(seed)
    s = [random.randint(0, 1) for i in range(len_msg)]
    bits2embed = np.bitwise_xor(msg2embed, np.uint8(s))
    # print('To embed:', bits2embed)

    # Step 2 data embedding via pair-wise DCT ordering
    # Embeddeding starts from the bottom-right corner
    img_marked = img_gray.copy()
    height, width = img_marked.shape
    cnt = 0
    delta = 10
    r0, c0 = 2, 3
    for row in np.arange(0, height - N, N):
        if cnt >= len_msg:
            break

        for col in np.arange(0, width - N, N):
            if cnt >= len_msg:
                break

            # embedding one bit in 1 pair of DCT coefficients
            block = np.array(img_marked[row:(row + N), col:(col + N)], np.float32)
            block_dct = cv2.dct(block)
            a, b = (block_dct[r0, c0], block_dct[c0, r0]) if block_dct[r0, c0] > block_dct[c0, r0] else (
            block_dct[c0, r0], block_dct[r0, c0])
            a += delta
            b -= delta
            block_dct[r0, c0] = (a if bits2embed[cnt] == 1 else b)
            block_dct[c0, r0] = (b if bits2embed[cnt] == 1 else a)

            cnt += 1
            img_marked[row:(row + N), col:(col + N)] = np.array(cv2.idct(block_dct), np.uint8)

    return img_marked, len_msg


def dct_extract(img_marked, len_msg, seed=2020):
    "An illustration of data extraction to the previous embedding,"
    " img_marked - of grayscale"
    " seed - the password for decryption"

    if len(img_marked.shape) > 2:
        print("Parameter img should be of grayscale")
        return img_marked

    N = 8
    height, width = img_marked.shape
    msg_embedded = ''
    cnt = 0
    r0, c0 = 2, 3
    for row in np.arange(0, height - N, N):
        if cnt >= len_msg:
            break

        for col in np.arange(0, width - N, N):
            if cnt >= len_msg:
                break

            # embedding one bit in 1 pair of DCT coefficients
            block = np.array(img_marked[row:(row + N), col:(col + N)], np.float32)
            block_dct = cv2.dct(block)
            msg_embedded += ('1' if block_dct[r0, c0] > block_dct[c0, r0] else '0')
            cnt += 1

    bits_extracted = [np.uint8(c) for c in msg_embedded]
    # print('Extracted:', bits_extracted)

    random.seed(seed)
    s = [random.randint(0, 1) for i in range(len_msg)]
    msgbits = np.bitwise_xor(bits_extracted, np.uint8(s))
    msg = bitseq2str(msgbits)

    return msg