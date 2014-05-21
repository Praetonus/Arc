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

import os
import pathlib

class FileStruct:
	def __init__(self, name, size, isDir):
		self.name = name
		self.size = size
		self.isDir = isDir

def archive(fileList, pathO):
	headers = makeHeaders(fileList)
	with open(pathO, "wb") as outputFile:
		outputFile.write(len(fileList).to_bytes(2, "little"))
		for elem in headers:
			name = elem.name.parts[len(elem.name.parts) - 1]
			outputFile.write(elem.isDir.to_bytes(1, "little"))
			outputFile.write(len(name).to_bytes(2, "little"))
			outputFile.write(bytes(name, "utf-8"))
			outputFile.write(elem.size.to_bytes(2, "little"))
		for elem in headers:
			if not elem.isDir:
				with elem.name.open("rb") as inputFile:
					outputFile.write(inputFile.read())

def makeHeaders(fileList):
	headers = [[], 2]
	for fileName in fileList:
		filePath = pathlib.Path(fileName)
		if not filePath.exists():
			raise FileNotFoundError("Error : file " + fileName + " does not exists.")
		makeFileHeader(filePath, headers, 0)
	return headers[0]

def makeFileHeader(filePath, headers, level):
	relativePath = pathlib.Path(filePath.parts[len(filePath.parts) - 1])
	for i in range(2, level + 2):
		relativePath = filePath.parts[len(filePath.parts) - i] / relativePath
	if filePath.is_dir():
		dirIndex = len(headers[0])
		i = 0
		headers[0].append(FileStruct(relativePath, 0, True))
		headers[1] += 5 + len(str(relativePath))
		for child in filePath.iterdir():
			makeFileHeader(child, headers, level + 1)
			i += 1
		headers[0][dirIndex].size = i
	elif filePath.is_file():
		headers[0].append(FileStruct(relativePath, filePath.stat().st_size, False))
		headers[1] += 5 + len(str(relativePath))

def extract(pathI):
	with open(pathI, "rb") as inputFile:
		headers = parseHeaders(inputFile)
		for elem in headers:
			if elem.isDir:
				pathlib.Path(elem.name).mkdir()
			else:
				with open(elem.name, "wb") as outputFile:
					outputFile.write(inputFile.read(elem.size))

def parseHeaders(inputFile):
	headers = []
	fileCount = int.from_bytes(inputFile.read(2), "little")
	for i in range(fileCount):
		parseFileHeader(inputFile, headers, pathlib.Path())
	return headers

def parseFileHeader(inputFile, headers, parentPath):
	isDir = bool(int.from_bytes(inputFile.read(1), "little"))
	name = pathlib.Path(inputFile.read(int.from_bytes(inputFile.read(2), "little")).decode("utf-8"))
	size = int.from_bytes(inputFile.read(2), "little")
	name = pathlib.Path(parentPath / name)
	headers.append(FileStruct(str(name), size, isDir))
	if isDir:
		for i in range(size):
			parseFileHeader(inputFile, headers, name)
