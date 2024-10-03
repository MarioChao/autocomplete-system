# Convert binary_search_tree to an AVL tree

# Imports

from binary_tree.binary_search_tree import BinaryTreeNode, BinarySearchTree

# Classes

class AvlTree(BinarySearchTree):
	# Node height

	def __get_node_avl_height(self, node: BinaryTreeNode):
		if not node:
			return 0
		return node.avl_height

	def __update_node_avl_height(self, node: BinaryTreeNode):
		node.avl_height = 1 + max(self.__get_node_avl_height(node.left), self.__get_node_avl_height(node.right))

	def get_balance(self, node: BinaryTreeNode):
		if not node:
			return 0
		return self.__get_node_avl_height(node.left) - self.__get_node_avl_height(node.right)

	# Rotate

	def __left_rotate(self, node: BinaryTreeNode):
		# Validate right child
		right_node = node.right
		if not (node and right_node):
			return

		# Rotate
		right_node.parent = node.parent
		node.right = right_node.left
		right_node.left = node

		# Root update
		if node == self.root:
			self.root = right_node

		# Update
		if node.right:
			node.set_right(node.right)
		if right_node.parent:
			right_node.parent.set_child(right_node)
		if right_node.left:
			right_node.set_left(right_node.left)
		if right_node.right:
			right_node.set_right(right_node.right)

		# Update height
		self.__update_node_avl_height(node)
		self.__update_node_avl_height(right_node)

	def __right_rotate(self, node: BinaryTreeNode):
		# Validate left child
		left_node = node.left
		if not (node and left_node):
			return

		# Rotate
		left_node.parent = node.parent
		node.left = left_node.right
		left_node.right = node

		# Root update
		if self.root == node:
			self.root = left_node

		# Update
		if node.left:
			node.set_left(node.left)
		if left_node.parent:
			left_node.parent.set_child(left_node)
		if left_node.left:
			left_node.set_left(left_node.left)
		if left_node.right:
			left_node.set_right(left_node.right)

		# Update height
		self.__update_node_avl_height(node)
		self.__update_node_avl_height(left_node)

	def resolve_rotate_node(self, node: BinaryTreeNode):
		# Get balance factors
		node_balance = self.get_balance(node)
		left_balance = self.get_balance(node.left)
		right_balance = self.get_balance(node.right)

		# Rotate cases
		if node_balance >= 2:
			### Left heavy ###
			if left_balance >= 0:
				# LL
				# print("LEFT LEFT")
				self.__right_rotate(node)
			else:
				# LR
				# print("LEFT RIGHT")
				self.__left_rotate(node.left)
				self.__right_rotate(node)
		elif node_balance <= -2:
			### Right heavy ###
			if right_balance <= 0:
				# RR
				# print("RIGHT RIGHT")
				self.__left_rotate(node)
			else:
				# RL
				# print("RIGHT LEFT")
				self.__right_rotate(node.right)
				self.__left_rotate(node)
		else:
			return False
		return True

	def avl_balance_tree(self, node: BinaryTreeNode):
		# Look up to root, update height, & rotate
		while node:
			# Update height
			self.__update_node_avl_height(node)

			# Resolve rotate
			rotate_result = self.resolve_rotate_node(node)
			if rotate_result:
				# print(f"Rotated node {node.value}")
				pass

			# Go to parent
			node = node.parent

	def insert_node(self, node: BinaryTreeNode):
		super().insert_node(node)
		self.avl_balance_tree(node)

	def delete_node(self, node: BinaryTreeNode):
		super().delete_node(node)
		self.avl_balance_tree(node)

# Example test

if __name__ == "__main__":
	# Initialize tree
	avl_tree = AvlTree()

	# Create nodes and build tree
	print("AVL tree 1")
	node_values = [5, 0, 1, 2, 2, 3, 4]
	for value in node_values:
		avl_tree.insert_node_with_value(value)
	avl_tree.display()

	# Create nodes and build tree
	avl_tree.init_empty()
	print("AVL tree 2")
	node_values = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
	for value in node_values:
		avl_tree.insert_node_with_value(value)
	avl_tree.display()
