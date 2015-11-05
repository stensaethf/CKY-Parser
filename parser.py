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
	parser() takes a sentence and parses it according to the given grammar.

	@params: filename where grammar is recorded,
			 sentence to be parsed.
	@return: n/a.
	"""
	grammar = getGrammar(grammar_filename)

	backpointer_lst = cky(grammar, sentence.split())

	printParseTree(backpointer_lst)

def cky(grammar, sentence):
	"""
	cky() takes sentence and parses it according to the provided grammar.

	@parmas: grammar (dictionary),
			 sentence (list of strings).
	@return: table (results from the algorithm),
			 backpointers for the solution.
	"""
	n = len(sentence)
	print(sentence)
	# Should we make this a dictionary? --> less memory.
	table = [[[] for i in range(n + 1)] for j in range(n + 1)]
	# Should we make this a dictionary? --> less memory.
	backpointers = [[[] for i in range(n + 1)] for j in range(n + 1)]

	for j in range(1, n + 1):
		# table[j - 1][j] += {A if A -> words[j] \in gram}
		# print(sentence[j - 1])
		for rule in grammar:
			# print(rule)
			# print(grammar[rule])
			# print(sentence[j - 1])
			if [sentence[j - 1]] in grammar[rule]:
				# print('entererd')
				# print(j)
				table[j - 1][j].append(rule)

		# print(table)
		# sys.exit()

		# Does this actually work or do we need an 'if'?
		for i in reversed(range(0, j - 1)): #(j - 2, 1) goes to 0
			# print(i)
			# print(j)
			# print()
			for k in range(i + 1, j): # goes to j - 1
				# table[i][j] += {A if A -> B C \in gram,
				# 				  B \in table[i][k]
				#				  C \in table[k][j]}

				# print(i)
				# print(k)
				# print(n)
				# print()

				for rule in grammar:
					# print()
					# print(rule)
					# print()
					for derivation in grammar[rule]:
						# print(derivation)
						# print()
						if len(derivation) == 2:
							B = derivation[0]
							C = derivation[1]
							# print(rule)
							# print(derivation)
							# print(B)
							# print(C)
							# print(table[i][k])
							# print(table[k][j])

							if B in table[i][k] and C in table[k][j]:
								print('entered')
								print(rule)
								print(B)
								print(C)
								if i == 0 and j == n:
									print('ypupyupupupup')
								print()
								table[i][j].append(rule)
							# print()
	
	print(table)
	print(table[0][n])
	sys.exit()
	return backpointers[0][n]

def printParseTree(backpointers):
	"""
	printParseTree() takes a parse tree in the form of a list of backpoitners
	and prints it out.

	@params: backpointers (list of multiple lists).
	@return: n/a.
	"""
	# Code

def getGrammar(grammar_filename):
	"""
	getGrammar() takes the filename of the file where our grammar rules are
	listed and reads these rules into a dictionary. The dictionary with the
	rules recorded is returned.
	
	Rules:
	- Lines beginning with # are comments.
	- All other lines are of the form X --> Y Z, X --> Y, X --> t.
	- Strings beginning with an uppercase letter are nonterminals.
	- Strings beginning with a lowercase letter are terminals.

	@params: filename of file where the grammar rules are listed.
	@return: dictionary w/ grammar rules.
	"""
	try:
		grammar_text = open(sys.argv[1], 'r')

	except: #Exception,e:
		# print e
		printError()

	grammar = {}
	# Loops over each line in the grammar file we were given to record the
	# grammar rules.
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
			right_side = rule[1].split()
			if len(right_side) > 2:
				printError(1)

			left_side = rule[0].split()
			if len(left_side) != 1:
				printError(1)
			elif left_side[0][0] != left_side[0][0].upper():
				printError(1)

			# If we have seen a derivation before, we add it to the list.
			if rule[0] in grammar:
				if right_side in grammar[rule[0]]:
					printError(1)
				else:
					# print('OTHER')
					# print(grammar[rule[0]])
					# print(right_side)
					grammar[rule[0]].append(right_side)
			# If we have not seen a derivation before we need to add it to
			# the dictionary.
			else:
				# print('RIGHT SIDE')
				# print(right_side)
				grammar[rule[0]] = [right_side]

		# print(grammar)

	# print(grammar)
	# sys.exit()

	return grammar

def printError(num):
	"""
	printError() prints out an error message and exits the program.

	@params: number that tells us where the error is coming from.
				0 --> general error.
				1 --> grammar file.
	@return: n/a.
	"""
	if num == 1:
		print('Error in the grammar file provided.')
	else:
		print('Error.')

	print('Usage: $ python3 parser.py <filename for grammar> <sentence>')

def main():
	if len(sys.argv) != 3:
		printError(0)
	elif not os.path.isfile(sys.argv[1]):
		printError(0)

	parser(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()