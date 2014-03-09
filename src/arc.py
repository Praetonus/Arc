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
	if len(sys.argv) < 4:
		syntaxError()
		return
	if sys.argv[1] == "-c":
		huffman.compress(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == "-d":
		huffman.decompress(sys.argv[2], sys.argv[3])
	else:
		syntaxError()

def syntaxError():
	print("Syntax error.")
	print("Usage : arc.py -c | -d input_file output_file")

if __name__ == "__main__":
	main()
