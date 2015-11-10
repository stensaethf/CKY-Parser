'''
parser.py
Frederik Roenn Stensaeth
11.05.15

A Python implementation of the CKY algorithm for generating parse trees, 
given a CFG (in almost-CNF) and a sentence.
'''

import sys
import os.path
from node import Node

def parser(grammar_filename, sentence):
	"""
	parser() takes a sentence and parses it according to the given grammar.

	@params: filename where grammar is recorded,
			 sentence to be parsed.
	@return: n/a.
	"""
	grammar = getGrammar(grammar_filename)

	nodes_back = cky(grammar, sentence.split())

	printParseTrees(nodes_back)

def cky(grammar, sentence):
	"""
	cky() takes sentence and parses it according to the provided grammar.

	@parmas: grammar (dictionary),
			 sentence (list of strings).
	@return: table (results from the algorithm),
			 list of root nodes for the solutions.
	"""
	n = len(sentence)
	# Should we make this a dictionary? --> less memory.
	table = [[[] for i in range(n + 1)] for j in range(n + 1)]
	# Should we make this a dictionary? --> less memory.
	nodes_back = [[[] for i in range(n + 1)] for j in range(n + 1)]

	for j in range(1, n + 1):
		# table[j - 1][j] += {A if A -> words[j] \in gram}
		for rule in grammar:
			if [sentence[j - 1]] in grammar[rule]:
				table[j - 1][j].append(rule)
				nodes_back[j - 1][j].append(
					Node(rule, None, None, sentence[j - 1]))

		# Loop over diagonally in the table and fill in the fields using
		# the rules of the grammar. We check subnodes to find out whether
		# a rule applies or not.
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

							# If A -> B C and B in table[i][k] and C in
							# table[k][j].
							if B in table[i][k] and C in table[k][j]:
								table[i][j].append(rule)

								for b in nodes_back[i][k]:
									for c in nodes_back[k][j]:
										if b.root == B and \
										   c.root == C:
											nodes_back[i][j].append(
												Node(rule, b, c, None))

	return nodes_back[0][n]

def printParseTrees(nodes_back):
	"""
	printParseTrees() takes a list of root nodes and prints the ones that
	start with an 'S'.

	@params: list of nodes.
	@return: n/a.
	"""
	check = False
	for node in nodes_back:
		if node.root == 'S':
			print(getParseTree(node, 3))
			print()
			check = True

	if not check:
		print('The given sentence is not valid according to the grammar.')

def getParseTree(root, indent):
	"""
	getParseTree() takes a root and constructs the tree in the form of a
	string. Right and left subtrees are indented equally, providing for
	a nice display.

	@params: root node and an indent factor (int).
	@return: tree, starting at the root provided, in the form of a string.
	"""
	if root.status:
		return '(' + root.root + ' ' + root.terminal + ')'

	# Calculates the new indent factors that we need to pass forward.
	new1 = indent + 2 + len(root.left.root) #len(tree[1][0])
	new2 = indent + 2 + len(root.right.root) #len(tree[2][0])
	left = getParseTree(root.left, new1)
	right = getParseTree(root.right, new2)
	return '(' + root.root + ' ' + left + '\n' \
			+ ' '*indent + right + ')'

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
		printError(1)

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
			elif len(right_side) == 0:
				printError(1)
			elif len(right_side) == 2:
				print(right_side)
				if right_side[0][0] == right_side[0][0].lower():
					printError(1)
				elif right_side[1][0] == right_side[1][0].lower():
					printError(1)
			else: # len(right_side) == 1
				if right_side[0][0] == right_side[0][0].lower():
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