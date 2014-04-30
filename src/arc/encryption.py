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

import hashlib

def encrypt(pathI, pathO, password):
	passHash = hashlib.sha1(password).digest()
	with open(pathO, "wb") as outputFile:
		outputFile.write(passHash)
		with open(pathI, "rb") as inputFile:
			string = inputFile.read()
			outputFile.write(xor(string, password))

def decrypt(pathI, pathO, password):
	with open(pathI, "rb") as inputFile:
		passHash = inputFile.read(20)
		if passHash != hashlib.sha1(password).digest():
			return False
		string = inputFile.read()
		with open(pathO, "wb") as outputFile:
		 	outputFile.write(xor(string, password))
	return True

def xor(string, password):
	retString = bytes()
	i = 0
	for char in string:
		retString += (char ^ password[i]).to_bytes(1, "little")
		++i
		if i == len(password):
			i = 0
	return retString
