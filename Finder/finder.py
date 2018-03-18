# -*- coding: utf-8 -*-

# Finder.
#
# A partir de um arquivo binario e de uma string de busca,
# o Finder eh capaz de encontrar possiveis ocorrencias desta
# string dentro do documento.
#
# @author Mateus Gabi Moreira

import binascii

class Finder():

	# metodo principal
	def run(self, file, string):
		print "Finder: rodando..."
		self.filename = 'SMario.sfc'
		self.relativeSearch('SMario.sfc', string)


	def fileToByteArray(self, filename):
		with open('SMario.sfc', 'rb') as f:
			hexdata = binascii.hexlify(f.read())

		return map(''.join, zip(hexdata[::2], hexdata[1::2]))


	# dado uma string, retorna array de valores relativos absolutos
	# o array sempre tera o tamanho da string - 1
	def getRelativeValuesByString(self, string):


		print "Finder: tentando obter os valores relativos de "+ str(string) +"..."

		#
		# pegamos a string e traduzimos em um array de hexadecimais, de forma que
		# cada posicao na string seja traduzida para um hexadecimal.
		#
		# Exemplo:
		# translateStringToHexadecimalArray("abc")
		#		returns [1, 2, 3]
		array_hexa = self.translateStringToHexadecimalArray(string)

		## calcula a diferenca ##
		i = 0
		relative_values = []

		while i < len(array_hexa) - 1:

			a = array_hexa[i]
			b = array_hexa[i + 1]

			_abs = self.absoluteDifferenceBetweenTwoHexadecimals(a, b)
			relative_values.append(_abs)
			i = i + 1

		print "Finder: valores relativos de " + str(string) + " é " + str(relative_values)

		return relative_values


	def getRelativeValuesBySFile(self):

		array_hexa = self.fileToByteArray(self.filename)

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


	# retorna um array de hexadecimais dado a string. Exemplo:
	# "string" => [73, 74, 72, 69, 6e, 67]
	def translateStringToHexadecimalArray(self, string):

		relative_values = []
		for x in string:
			relative_values.append(str(x).encode("hex"))

		return relative_values


	# faz o trabalho sujo da busca
	def relativeSearch(self, filename, string):


		print "Finder: Fazendo a busca de " + str(string) + " em " + str(filename)

		# pegamos os valores relativos da string
		relative_array = self.getRelativeValuesByString(string)

		# pegamos o array de byte do arquivo
		byte_array = self.getRelativeValuesBySFile()


		last = self.findLastOccourInAray(byte_array, relative_array)

		byte_array = self.fileToByteArray(self.filename)

		print byte_array[last:last+len(relative_array)+1]

		


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
					print "match on i = " + str(i)
					last_occour = i


			i = i + 1
			j = 0

		return last_occour


	# retorna a difereça absoluta (em decimal) entre dois hexas. 
	def absoluteDifferenceBetweenTwoHexadecimals(self, a, b):
		
		_a = int(a, 16)
		_b = int(b, 16)

		return abs(_a - _b)


#
# prints an array
def printArray(msg, array):

	a = ""
	for x in array:
		a = a + ", " + str(x)


	print msg + " {" + a[2:] + "}" 



if __name__ == '__main__':
	finder = Finder()

	finder.run("file.fl", "elcome")