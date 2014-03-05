#!/usr/bin/python3.3
#-*- coding: utf-8 -*-

########################################################################
# Copyright 2014 Benoît Vey                                            #
#                                                                      #
# This file is part of Arc.                                            #
#                                                                      #
# Arc is free software: you can redistribute it and/or modify          #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# Arc is distributed in the hope that it will be useful,               #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with Arc.  If not, see <http://www.gnu.org/licenses/>.         #
########################################################################

import sys
from arc import huffman

def main():
	if len(sys.argv) < 3:
		syntaxError()
		return
	with open(sys.argv[1], "rb") as inputFile:
		freqs = huffman.frequencies(inputFile)
		rootNode = huffman.makeTree(freqs)
		codes = huffman.makeCodes(rootNode)
		inputFile.seek(0)
		cmpStr = huffman.compressedString(inputFile, codes)
	with open(sys.argv[2], "wb") as outputFile:
		huffman.write(outputFile, codes, cmpStr)

def syntaxError():
	print("Syntax error.")
	print("Usage : arc.py input_file output_file")

if __name__ == "__main__":
	main()
