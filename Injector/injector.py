# -*- coding: utf-8 -*-
"""
Injector.

A partir de um arquivo binario, de uma tabela binaria gerada com o Finder,
e um arquivo de substituição, o Injector é capaz de injetar um texto
no binario trocando o texto in-game

O Injector faz automaticamente a adequação do tamanho do texto ao tamanho da caixa,
truncando se maior e colocando corretamente as quebras de linha


@author Yan Uehara
"""

from __future__ import print_function
import os
import sys
import binascii
import pickle


class Injector:
    def __init__(self, sfc, tbl, substituto):
        self.sfc = sfc
        self.tbl = tbl
        self.substituto = substituto
        self.bytefile = None
        self.dictionary = None
        self.inv_dictionary = None
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
            del self.dictionary["offset"]
            self.inv_dictionary = {v: k for k, v in self.dictionary.items()}

    def inject(self):
        _txt = []
        char_count = 0
        with open(self.substituto, "r") as _txtfile:
            _txt = _txtfile.read().replace('\n', '')

        print(len(self.bytefile))
        for numero_linha in xrange(1, 9):
            for numero_coluna in xrange(1, 18):
                try:
                    self.bytefile[self.offset] = self.inv_dictionary[_txt[char_count]]
                    if numero_coluna is 18:
                        self.bytefile[self.offset] = self.inv_dictionary[_txt[char_count]+"\n"]
                except IndexError:
                    pass
                char_count = char_count + 1
                self.offset = self.offset + 1

        print(len(self.bytefile))
        # with open(self.sfc.replace(".sfc", ".modified.sfc"), "wb") as sfc_file:
        sfc_file = open(self.sfc.replace(".sfc", ".modified.sfc"), "wb")
        for byte in self.bytefile:
            sfc_file.write(
                binascii.unhexlify(byte)
            )

    """
    Entry-point da classe
    """
    def run(self):
        self.fileToByteArray()
        self.readBinaryTbl()
        self.inject()


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("Use: python extractor.py [sfc] [tbl] [substituto]")
        sys.exit(1)

    sfc = sys.argv[1]
    tbl = sys.argv[2]
    substituto = sys.argv[3]

    if os.path.exists(sfc) and os.path.isfile(tbl):
        inj = Injector(sfc, tbl, substituto)
        inj.run()
