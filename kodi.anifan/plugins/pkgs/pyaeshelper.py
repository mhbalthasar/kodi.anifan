# -*- coding:utf-8 -*-
import io
import sys
import base64
import pyaes

class PYAESCipher(object):
    def __init__(self, key, iv):

        self.key = key.encode('utf-8') if not isinstance(key, bytes) else key
        self.iv = iv.encode('utf-8') if not isinstance(iv, bytes) else iv

    def pkcs7_unpadding(self, string):

        return string[0:-ord(string[-1])]

    def pkcs7_padding(self, s, block_size=16):
        """假设数据长度需要填充n(n>0)个字节才对齐，那么填充n个字节，每个字节都是n;
        如果数据本身就已经对齐了，则填充一块长度为块大小的数据，每个字节都是块大小
        """

        bs = block_size
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs).encode()

    def split_to_data_blocks(self, byte_str, block_size=16):

        length = len(byte_str)
        j, y = divmod(length, block_size)
        blocks = []
        shenyu = j * block_size
        for i in range(j):
            start = i * block_size
            end = (i + 1) * block_size
            blocks.append(byte_str[start:end])
        stext = byte_str[shenyu:]
        if stext:
            blocks.append(stext)
        return blocks

    def encrypt(self, plaintext):

        ciphertext = b''
        cbc = pyaes.AESModeOfOperationCBC(self.key, self.iv)
        if not isinstance(plaintext, bytes):
            plaintext = plaintext.encode('utf-8')
        blocks = self.split_to_data_blocks(self.pkcs7_padding(plaintext))
        for b in blocks:
            ciphertext = ciphertext + cbc.encrypt(b)
        base64_text = base64.b64encode(ciphertext)
        return base64_text

    def decrypt(self, ciphertext):

        cbc = pyaes.AESModeOfOperationCBC(self.key, self.iv)
        if not isinstance(ciphertext, bytes):
            ciphertext = ciphertext.encode('utf8')
        ciphertext = base64.b64decode(ciphertext)
        ptext = b""
        for b in self.split_to_data_blocks(ciphertext):
            ptext = ptext + cbc.decrypt(b)
        return self.pkcs7_unpadding(ptext.decode())

