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

import os

def archive(fileList, pathO):
	offsets = calculateOffsets(fileList)
	with open(pathO, "wb") as outputFile:
		outputFile.write(len(fileList).to_bytes(1, "little"))
		for i in range(len(fileList)):
			outputFile.write(len(fileList[i]).to_bytes(1, "little"))
			outputFile.write(bytes(fileList[i], "utf-8"))
			outputFile.write(offsets[i].to_bytes(1, "little"))
		for fileName in fileList:
			with open(fileName, "rb") as inputFile:
				outputFile.write(inputFile.read())

def calculateOffsets(fileList):
	offsets = []
	filesSize = 0
	headersSize = 1
	for fileName in fileList:
		headersSize += len(fileName) + 2
		with open(fileName, "rb") as inputFile:
			offsets.append(filesSize)
			inputFile.seek(0, os.SEEK_END)
			filesSize += inputFile.tell()
	for i in range(len(offsets)):
		offsets[i] += headersSize
	return offsets

def extract(pathI):
	with open(pathI, "rb") as inputFile:
		headers = parseHeaders(inputFile)
		for fileName, offset in headers.items():
			inputFile.seek(offset[0])
			with open(fileName, "wb") as outputFile:
				if offset[1] == 0:
					outputFile.write(inputFile.read())
				else:
					outputFile.write(inputFile.read(offset[1]))

def parseHeaders(inputFile):
	headers = {}
	fileCount = int.from_bytes(inputFile.read(1), "little")
	prevName = str()
	prevOffset = 0
	for i in range(fileCount):
		nameSize = int.from_bytes(inputFile.read(1), "little")
		name = inputFile.read(nameSize).decode("utf-8")
		offset = int.from_bytes(inputFile.read(1), "little")
		headers[name] = [offset, 0]
		if prevName != "":
			headers[prevName][1] = offset - headers[prevName][0]
		prevName = name
		prevOffset = offset
	return headers
