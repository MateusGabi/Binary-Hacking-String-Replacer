# -*- coding: utf-8 -*-
"""
Extractor.

A partir de um arquivo binario e de uma tabela binaria gerada com o Finder,
o Extractor é capaz de extrair todo o texto de um binario
a partir de um offset inicial marcado pelo finder

@author Yan Uehara
"""

from __future__ import print_function
import os
import sys
import binascii
import pickle


class Extractor:
    def __init__(self, sfc, tbl):
        self.sfc = sfc
        self.tbl = tbl
        self.bytefile = None
        self.dictionary = None
        self.offset = 0

    """
    pega o arquivo e retorna seus bytes em um array de bytes
    """
    def fileToByteArray(self):
        with open(self.sfc, 'rb') as f:
            hexdata = binascii.hexlify(f.read())

        self.bytefile = map(''.join, zip(hexdata[::2], hexdata[1::2]))

    """
    Lê a tabela binaria de conversao
    """
    def readBinaryTbl(self):
        with open(self.tbl, 'rb') as btblobj:
            self.dictionary = pickle.Unpickler(btblobj).load()
            self.offset = self.dictionary["offset"]

    """
    Faz um dump para um arquivo dos textos encontrados no arquivo sfc
    """
    def dumpToFileWithOffset(self):
        _fileobj = open(self.sfc.replace("sfc", "extracted.txt"), "w")
        for byte in xrange(self.offset, len(self.bytefile)):
            if self.bytefile[byte] in self.dictionary:
                _fileobj.write(self.dictionary[self.bytefile[byte]])
            self.offset = self.offset + 1
        _fileobj.close()

    """
    Entry-point da classe
    """
    def run(self):
        self.fileToByteArray()
        self.readBinaryTbl()
        self.dumpToFileWithOffset()


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Use: python extractor.py [sfc] [tbl]")
        sys.exit(1)

    sfc = sys.argv[1]
    tbl = sys.argv[2]

    if os.path.exists(sfc) and os.path.isfile(sfc) and os.path.exists(tbl) and os.path.isfile(tbl):
        ext = Extractor(sfc, tbl)
        ext.run()
