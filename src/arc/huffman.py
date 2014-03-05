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

import ctypes

class Node:
	def __init__(self, char, weight):
		self.leftLeaf = None
		self.rightLeaf = None
		self.char = char
		self.weight = weight
		self.isEnd = True
		self.pastLeft = True
		self.pastRight = True

def frequencies(inputFile):
	freqs = {}
	char = bytes()
	while 1:
		char = inputFile.read(1)
		if char == b"":
			break
		if char in freqs:
			freqs[char] += 1
		else:
			freqs[char] = 1
	return freqs

def makeTree(freqs):
	nodes = []
	for char, weight in freqs.items():
		nodes.append(ctypes.pointer(ctypes.py_object(Node(char, weight))))
	
	while len(nodes) > 1:
		node1 = nodes[0]
		nodes.remove(nodes[0])
		node2 = nodes[0]
		nodes.remove(nodes[0])
		newNode = ctypes.pointer(ctypes.py_object(Node(b"", node1[0].weight + node2[0].weight)))
		newNode[0].leftLeaf = node1
		newNode[0].rightLeaf= node2
		newNode[0].isEnd = False
		newNode[0].pastLeft = False
		newNode[0].pastRight = False
		i = 0
		while i < len(nodes) and nodes[i][0].weight < newNode[0].weight:
			i += 1
		nodes.insert(i, newNode)
	return nodes[0]

def makeCodes(root):
	codes = {}
	while 1:
		currentNode = root
		code = str()
		blocked = False
		while not currentNode[0].isEnd and not blocked:
			if not currentNode[0].pastLeft:
				if currentNode[0].leftLeaf[0].pastLeft and currentNode[0].leftLeaf[0].pastRight:
					currentNode[0].pastLeft = True
				currentNode = currentNode[0].leftLeaf
				code += "0"
			elif not currentNode[0].pastRight:
				if currentNode[0].rightLeaf[0].pastLeft and currentNode[0].rightLeaf[0].pastRight:
					currentNode[0].pastRight = True
				currentNode = currentNode[0].rightLeaf
				code += "1"
			else:
				blocked = True
		if currentNode[0].isEnd:
			codes[currentNode[0].char] = code
			currentNode[0].pastLeft = True
			currentNode[0].pastRight = True
		if blocked and currentNode == root:
			break
	return codes

def compressedString(inputFile, codes):
	cmpStr = str()
	char = bytes()
	while 1:
		char = inputFile.read(1)
		if char == b"":
			break
		if char in codes:
			cmpStr += codes[char]
	while len(cmpStr) % 8 != 0:
		cmpStr += "0"
	return cmpStr

def write(outputFile, codes, cmpStr):
	outputFile.write(len(codes).to_bytes(1, "little"))
	for char, code in codes.items():
		outputFile.write(char)
		if (code[0] == "0"):
			while len(code) < 8:
				code = "1" + code
		else:
			while len(code) < 8:
				code = "0" + code
		value = 0
		for i in range(0, 8):
			if code[7 - i] == "1":
				value += 2 ** i
		outputFile.write(value.to_bytes(1, "little"))
	
	value = 0
	count = 0
	for char in cmpStr:
		if char == "1":
			value += 2 ** (7 - count)
		if count == 7:
			outputFile.write(value.to_bytes(1, "little"))
			value = 0
			count = 0
		else:
			count += 1
