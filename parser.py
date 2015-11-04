'''
parser.py
Frederik Roenn Stensaeth
11.04.15

A Python implementation of the CKY algorithm for generating parse trees, 
given a CFG (in almost-CNF) and a sentence.
'''

import sys
import os.path

def parser(grammar_filename, sentence):
	"""
	parser() xx.

	@params: xx.
	@return: xx.
	"""
	grammar = getGrammar(grammar_filename)

	# Code.

	return None

def getGrammar(grammar_filename):
	"""
	getGrammar() xx.
	
	Rules:
	- Lines beginning with # are comments.
	- All other lines are of the form X --> Y Z, X --> Y, X --> t.
	- Strings beginning with an uppercase letter are nonterminals.
	- Strings beginning with a lowercase letter are terminals.

	@params: xx.
	@return: xx.
	"""
	try:
		grammar_text = open(sys.argv[1], 'r')

	except Exception,e:
		# print e
		printError()

	grammar = {}
	for line in grammar_text:
		# We do not want to read the comments.
		if line[0] != '#':
			# Finds the different parts of the rule.
			rule = line.split('->')
			if len(rule) != 2:
				printError(1)

			rule[0] = rule[0].strip()
			rule[1] = rule[1].strip()

			# Makes sure the grammar is of the proper form.
			right = rule[1].split()
			if len(right) > 2:
				printError(1)

			Xx

	# Code.

	return None

# printError
	# 0 --> normal error
	# 1 --> grammar file

def main():
	if len(sys.argv) != 3:
		printError(0)
	elif not os.path.isfile(sys.argv[1]):
		printError(0)

	parser(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()