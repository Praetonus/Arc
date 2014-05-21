#!/usr/bin/python3.4
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
from arc import archive
from arc import encryption

def main():
	if len(sys.argv) == 2:
		if sys.argv[1] == "-h":
			usage()
	elif len(sys.argv) == 3:
		if sys.argv[1] == "-x":
			archive.extract(sys.argv[2])
		else:
			print("Syntax error.")
			usage()
	elif len(sys.argv) >= 4:
		if sys.argv[1] == "-a":
			fileList = list(sys.argv)
			for i in range(3):
				fileList.pop(0)
			archive.archive(fileList, sys.argv[2])
		elif sys.argv[1] == "-c":
			huffman.compress(sys.argv[2], sys.argv[3])
		elif sys.argv[1] == "-d":
			huffman.decompress(sys.argv[2], sys.argv[3])
		elif sys.argv[1] == "-e":
		  	password = input("Enter password : ").encode("utf-8")
		  	encryption.encrypt(sys.argv[2], sys.argv[3], password)
		elif sys.argv[1] == "-p":
			password = input("Enter password : ").encode("utf-8")
			if not encryption.decrypt(sys.argv[2], sys.argv[3], password):
				print("Wrong password.")
		else:
			print("Syntax error.")
			usage()
	else:
		print("Syntax error.")
		usage()

def usage():
	print("Usage :")
	print("\tarc.py -h : Display this message")
	print("\tarc.py -a archive_name input_file ... : Archive files")
	print("\tarc.py -x archive_name : Extract archive")
	print("\tarc.py -c input_file output_file : Compress file")
	print("\tarc.py -d input_file output_file : Decompress file")
	print("\tarc.py -e input_file output_file : Encrypt file")
	print("\tarc.py -p input_file output_file : Decrypt file")

if __name__ == "__main__":
	main()
