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
import pickle

class Finder():

	def __init__(self, filename, string):
		self.filename = filename
		self.string = string


		self.dictionary = {}

	# metodo principal
	def run(self):

		string_relative = self.getRelativeValuesByString()
		file = self.fileToByteArray()

		# print(string_relative)
		# sys.exit()


		file_size = len(file)
		for i in range(1, file_size - 1):
			diff_file = self.absoluteDifferenceBetweenTwoHexadecimals(file[i - 1], file[i])
			j = 0
			_i = i + 1
			string_on_file = []
			string_on_file.append(file[i-1])
			while diff_file == string_relative[j]:
				diff_file = self.absoluteDifferenceBetweenTwoHexadecimals(file[_i - 1], file[_i])
				string_on_file.append(file[_i-1])
				_i = _i + 1
				j = j + 1

				if j == len(string_relative):
					print("match on: " + str(_i))

					self.generateTBL(string_on_file[0], self.string[0], _i - len(self.string) - 1 )

					# for s, v in zip(string_on_file, self.string):
					# 	self.dictionary[s] = v

					print(self.dictionary)
					print(string_on_file)



					try:
						print(self.dictionary['a'])
					except KeyError as e:
						print('', end='')
					break

		

		# for a in file:
		# 	print(self.dictionary.get(a, ""), end='')


						

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

	# retorna a difereça absoluta (em decimal) entre dois hexas. 
	def absoluteDifferenceBetweenTwoHexadecimals(self, a, b):
		
		_a = int(a, 16)
		_b = int(b, 16)

		return abs(_a - _b)


	def generateTBL(self, hexadecimal, value, offset):
		letter_in_ascii = ord(value)
		hexadecimal_in_decimal = int(hexadecimal, 16)

		offset_minuscula = hexadecimal_in_decimal - letter_in_ascii
		offset_maiuscula = 19 - 84
		offset_minuscula_eol = 210 - 115

		"""letras minusculas"""
		for x in xrange(97, 122):
			a = hex(x + offset_minuscula).split('x')[-1]
			self.dictionary[""+str(a)+""] = chr(x)

		""" letras maiusculas"""
		for x in xrange(65, 90):
			a = hex(x + offset_maiuscula).split('x')[-1]
			self.dictionary[""+str(a)+""] = chr(x)

		""" letras minusculas com eol"""
		for x in xrange(97, 122):
			a = hex(x + offset_minuscula_eol).split('x')[-1]
			self.dictionary[""+str(a)+""] = chr(x) + "\n"

		""" 1f é Space """
		self.dictionary['1f'] = " "
		self.dictionary['1a'] = "!"
		self.dictionary['1b'] = "."


		""" letras maiusculas perdidas"""
		self.dictionary['03'] = 'D'
		self.dictionary['08'] = 'I'
		self.dictionary['0b'] = 'L'
		self.dictionary['0c'] = 'M'
		self.dictionary['0d'] = 'N'
		self.dictionary['0e'] = 'O'
		self.dictionary['0f'] = 'P'
		self.dictionary['10'] = 'Q'
		self.dictionary['11'] = 'R'
		self.dictionary['12'] = 'S'

		self.dictionary['offset'] = offset

		_filename = self.filename.replace("sfc","btbl")
		_fileobj = open(_filename, "wb")
		pickle.Pickler(_fileobj, protocol=2).dump(self.dictionary)


		""" 13 é T"""
		# self

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