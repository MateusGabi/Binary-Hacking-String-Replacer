# -*- coding: utf-8 -*-
"""
Finder.

A partir de um arquivo binario e de uma string de busca,
o Finder eh capaz de encontrar possiveis ocorrencias desta
string utilizando busca relativa dentro do documento.

@author Mateus Gabi Moreira
"""
from __future__ import print_function
import binascii
import sys
import os.path

class Finder():

	def __init__(self, filename, string):
		self.filename = filename
		self.string = string

	# metodo principal
	def run(self):

		self.relativeSearch()


	"""
	pega o arquivo e retorna seus bytes em um array de bytes
	"""
	def fileToByteArray(self):
		with open(self.filename, 'rb') as f:
			hexdata = binascii.hexlify(f.read())

		return map(''.join, zip(hexdata[::2], hexdata[1::2]))

	"""
	Retorna array de valores relativos absolutos da string de busca. O array sempre
	terá o tamanho da string - 1.
	"""
	def getRelativeValuesByString(self):

		#
		# pegamos a string e traduzimos em um array de hexadecimais, de forma que
		# cada posicao na string seja traduzida para um hexadecimal.
		#
		# Exemplo:
		# translateStringToHexadecimalArray("abc")
		#		returns [1, 2, 3]
		array_hexa = self.translateStringToHexadecimalArray()

		"""
		TODO método que encapsula o cálculo de valores relativos
		"""
		## calcula a diferenca ##
		i = 0
		relative_values = []

		while i < len(array_hexa) - 1:

			a = array_hexa[i]
			b = array_hexa[i + 1]

			_abs = self.absoluteDifferenceBetweenTwoHexadecimals(a, b)
			relative_values.append(_abs)
			i = i + 1

		print("Finder: valores relativos de " + str(self.string) + " é " + str(relative_values))

		return relative_values


	"""
	Retorna os valores relativos do arquivo passado como input
	"""
	def getRelativeValuesBySFile(self):

		array_hexa = self.fileToByteArray()

		"""
		TODO método que encapsula o cálculo de valores relativos
		"""
		## calcula a diferenca ##
		i = 0
		relative_values = []

		while i < len(array_hexa) - 1:

			a = array_hexa[i]
			b = array_hexa[i + 1]

			_abs = self.absoluteDifferenceBetweenTwoHexadecimals(a, b)
			relative_values.append(_abs)
			i = i + 1

		return relative_values


	"""
	retorna um array de hexadecimais dado a string. Exemplo:
	"string" => [73, 74, 72, 69, 6e, 67]
	"""
	def translateStringToHexadecimalArray(self):

		relative_values = []
		for x in self.string:
			relative_values.append(str(x).encode("hex"))

		return relative_values


	# faz o trabalho sujo da busca
	def relativeSearch(self):


		print("Finder: Fazendo a busca de " + str(self.string) + " em " + str(self.filename))

		# pegamos os valores relativos da string
		relative_array = self.getRelativeValuesByString()

		# pegamos o array de byte do arquivo
		byte_array = self.getRelativeValuesBySFile()


		last = self.findLastOccourInAray(byte_array, relative_array)

		byte_array = self.fileToByteArray()

		array_char_string = [str(s) for s in self.string]
		array_hex_file = byte_array[last:last+len(relative_array)+1]

		print(array_hex_file);
		print(byte_array[last - 2])
		# sys.exit(1);

		array_string_translate_to_hex = self.translateStringToHexadecimalArray(self.string)

		offset = int(array_string_translate_to_hex[0], 16) - int(array_hex_file[0], 16)

		"""
		TODO: validador: um for que percorre todos os valores vendo se o offset nao mudou
		"""
		offset = hex(offset)

		for byte in byte_array:

			""" Caracteres Maiusculos e com início de linha começam em 00"""
			b = int(byte,16)
			if b >= 0 and b < 5:
				b = hex( b + int('41', 16))
				b = int(b, 16)
				print("")
				print("%c" % b, end='')


			# if b >= 187 and b < :
			# 	pass

			else:

				sume = hex(int(byte,16)+int(offset,16))
				sume = int(sume, 16)
				
				if sume > 45 and sume < 90:
					sume = sume + 32

				if sume < 0:
					print('<>', end='')

				else:

					if sume == 91:
						print('!', end='')

					# espaço no texto
					elif sume == 96:
						print(' ', end='')

					else:
						try:
							print("%c" % sume, end='')
						except Exception as e:
							print('#')

		
		

	"""
	Encontra última ocorrência do array_b dentro do array_a. Isso serve para
	retornar a última possível palavra encontrada.
	"""
	def findLastOccourInAray(self, array_a, array_b):

		last_occour = 0


		j = 0
		i = 0
		while i < len(array_a) - 1:
			a = array_a[i]
			b = array_b[0]

			if a == b:
				j = 1
				_i = i + 1
				while j < len(array_b) - 1:
					c = array_a[_i]
					d = array_b[j]

					if c == d:
						_i = _i + 1
						j = j + 1
					else:
						break


				if j == len(array_b) - 1:
					print("match on i = " + str(i))
					last_occour = i


			i = i + 1
			j = 0

		return last_occour


	# retorna a difereça absoluta (em decimal) entre dois hexas. 
	def absoluteDifferenceBetweenTwoHexadecimals(self, a, b):
		
		_a = int(a, 16)
		_b = int(b, 16)

		return abs(_a - _b)




if __name__ == '__main__':

	if len(sys.argv) != 3:
		print("Use: python finder.py [filename] [string] | grep -A2 [string]")
		sys.exit(1)
		

	filename = sys.argv[1]
	string = sys.argv[2]


	if os.path.exists(filename) and os.path.isfile(filename):

		finder = Finder(filename, string)

		finder.run()

	else:

		print("Arquivo \""+ filename +"\" não encontrado para a busca por \""+ string +"\".")
		sys.exit(1)