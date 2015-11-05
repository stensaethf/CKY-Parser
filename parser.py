'''
parser.py
Frederik Roenn Stensaeth
11.04.15

A Python implementation of the CKY algorithm for generating parse trees, 
given a CFG (in almost-CNF) and a sentence.
'''

import sys
import os.path

class Node:
	"""
	Node xx
	"""

	def __init__(self, root, left, right, terminal):
		"""
		"""
		self.root = root
		self.left = left
		self.right = right
		self.terminal = terminal
		if terminal == None:
			self.status = False
		else:
			self.status = True

	# def __init__(self, root, terminal):
	# 	"""
	# 	"""
	# 	self.root = root
	# 	self.left = None
	# 	self.right = None
	# 	self.terminal = terminal
	# 	self.status = True

	def getRoot(self):
		"""
		"""
		return self.root

	def getLeft(self):
		"""
		"""
		return self.left

	def getRight(self):
		"""
		"""
		return self.right

	def isTerminal(self):
		"""
		"""
		return self.status

	def getTerminal(self):
		"""
		"""
		return self.terminal

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
	backpointers = [[{} for i in range(n + 1)] for j in range(n + 1)]
	nodes_back = [[[] for i in range(n + 1)] for j in range(n + 1)]

	for j in range(1, n + 1):
		# table[j - 1][j] += {A if A -> words[j] \in gram}
		for rule in grammar:
			if [sentence[j - 1]] in grammar[rule]:
				table[j - 1][j].append(rule)
				backpointers[j - 1][j][rule] = [rule, sentence[j - 1]]
				nodes_back[j - 1][j].append(Node(rule, None, None, sentence[j - 1]))

		# Does this actually work or do we need an 'if'?
		for i in reversed(range(0, j - 1)): #(j - 2, 1) goes to 0
			for k in range(i + 1, j): # goes to j - 1
				# table[i][j] += {A if A -> B C \in gram,
				# 				  B \in table[i][k]
				#				  C \in table[k][j]}
				for rule in grammar:
					for derivation in grammar[rule]:
						if len(derivation) == 2:
							B = derivation[0]
							C = derivation[1]

							if B in table[i][k] and C in table[k][j]:
								table[i][j].append(rule)
								if rule in backpointers[i][j]:
									pass # Do nothing.
									# backpointers[i][j][rule].append(1)
								else:
									backpointers[i][j][rule] = \
										[rule, backpointers[i][k][B], \
										 backpointers[k][j][C]]

								for b in nodes_back[i][k]:
									for c in nodes_back[k][j]:
										if b.getRoot() == B and c.getRoot() == C:
											nodes_back[i][j].append(Node(rule, b, c, None))

	
	# print(table)
	# print()
	# print(table[0][n])
	# print()
	print(backpointers)
	print()
	print(backpointers[0][n]['S'])
	print(nodes_back[0][n])
	for node in nodes_back[0][n]:
		print(node.isTerminal())
	# sys.exit()
	return backpointers[0][n]

def printParseTree(backpointer_dict):
	"""
	printParseTree() takes a parse tree in the form of a list of backpoitners
	and prints it out.

	@params: backpointers (dictionary of multiple lists).
	@return: n/a.
	"""
	if 'S' not in backpointer_dict:
		print('The given sentence was not valid according to the grammar.')
	else:
		S = backpointer_dict['S']
		# print(len(S))
		# result = '(S ' + constructSubTree(S[1], 5 + len(S[1][0])) + '\n' \
		# 		 + ' '*3 + constructSubTree(S[2], 5 + len(S[2][0])) + ')'
		print(constructSubTree(S, 3))

def constructSubTree(tree, indent):
	"""
	constructSubTree() takes a tree and constructs the sub trees of that
	tree. The result is a string that can be printed out to nicely show what
	the tree looks like.

	@params: a tree (root or root and subtrees) and a number to indent by.
	@return: sub tree in the form of a string.
	"""
	result = ''
	if len(tree) == 2:
		if tree[1] == tree[1].lower():
			# Terminal value was reached
			result = '(' + tree[0] + ' ' + tree[1] + ')'
		else:
			# Nonterminal to single nonterminal
			new = indent + 2 + len(tree[1][0])
			result = '(' + tree[0] + ' ' + constructSubTree(tree[1], new) + ')'
	else:
		# print(tree[0])
		# print(len(tree[0]))
		# print(indent)
		new1 = indent + 2 + len(tree[1][0])
		new2 = indent + 2 + len(tree[2][0])
		result = '(' + tree[0] + ' ' + constructSubTree(tree[1], new1) \
				 + '\n' + ' '*indent + constructSubTree(tree[2], new2) + ')'

	return result

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
					grammar[rule[0]].append(right_side)
			# If we have not seen a derivation before we need to add it to
			# the dictionary.
			else:
				grammar[rule[0]] = [right_side]

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