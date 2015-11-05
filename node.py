'''
parser.py
Frederik Roenn Stensaeth
11.05.15

A Node class used for a Python implementation of the CKY algorithm for 
generating parse trees, given a CFG (in almost-CNF) and a sentence.
'''

class Node:
	"""
	The Node clas functions as a way to construct a tree using nodes that have
	children.

	Methods:
	- root
	- left
	- right
	- status
	- terminal
	"""

	def __init__(self, root, left, right, end):
		"""
		Constructor for the Node class. Root, left, right, terminal and status
		are set up here. Status is infered from whether a terminal value is
		provided or not.
		"""
		self._root = root
		self._left = left
		self._right = right
		self._terminal = end
		self._status = True
		if end == None:
			self._status = False

	@property
	def root(self):
		"""
		root allows the user to get the root of the node.

		@params: n/a.
		@return: the root.
		"""
		return self._root

	@property
	def left(self):
		"""
		left allows the user to get the left subtree of the node.

		@params: n/a.
		@return: the left subtree.
		"""
		return self._left

	@property
	def right(self):
		"""
		right allows the user to get the right subtree of the node.

		@params: n/a.
		@return: the right subtree.
		"""
		return self._right

	@property
	def status(self):
		"""
		status allows the user to get the status of the node.

		@params: n/a.
		@return: boolean for whether it is a terminal node or not.
		"""
		return self._status

	@property
	def terminal(self):
		"""
		terminal allows the user to get the terminal value of the node.

		@params: n/a.
		@return: the terminal value.
		"""
		return self._terminal

		