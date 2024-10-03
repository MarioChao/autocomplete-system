# Types

type NodeValueType = str

# Comparison functions

def is_left(parent_value: NodeValueType, child_value: NodeValueType):
	return child_value <= parent_value

# Node class

class BinaryTreeNode:
	def __init__(self, value=0) -> None:
		self.parent = None
		self.left = None
		self.right = None
		self.value = value
		self.avl_height = 1

	def set_left(self, other: "BinaryTreeNode"):
		self.left = other
		other.__set_parent(self)

	def set_right(self, other: "BinaryTreeNode"):
		self.right = other
		other.__set_parent(self)

	def set_child(self, other: "BinaryTreeNode"):
		if is_left(self.value, other.value):
			self.set_left(other)
		else:
			self.set_right(other)

	def __set_parent(self, other: "BinaryTreeNode"):
		self.parent = other

	def remove_child(self, other: "BinaryTreeNode"):
		if self.left == other:
			self.left = None
		if self.right == other:
			self.right = None

	def set_value(self, value: NodeValueType):
		self.value = value

	def display_subtree(self, depth=0):
		if (depth>10): return
		print(f"{"":{depth * 3}} {self.value:3}")
		if self.left:
			self.left.display_subtree(depth + 1)
		else:
			print(f"{"":{(depth + 1) * 3}} {"-":>3}")
		if self.right:
			self.right.display_subtree(depth + 1)
		else:
			print(f"{"":{(depth + 1) * 3}} {"-":>3}")

	# Traversals

	# Exercise 2

	def traverse_inorder(self):
		result = []

		# Loop
		temp_nodes = []
		node: BinaryTreeNode = self
		while node or temp_nodes:
			# Handle left side
			while node:
				temp_nodes.append(node)
				node = node.left

			# Get next temporary node
			node = temp_nodes.pop()

			# Store value
			result.append(node.value)

			# Loop from right subtree
			node = node.right

		return result

	# Exercise 3

	def get_depth(self):
		max_depth = 0

		# Iterative DFS (stack)
		temp_node_info = [(self, 1)]
		while temp_node_info:
			# Get node
			node, depth = temp_node_info.pop()

			# Validate node
			if not node:
				continue

			# Update result
			max_depth = max(max_depth, depth)

			# Push child nodes
			if node.left:
				temp_node_info.append((node.left, depth + 1))
			if node.right:
				temp_node_info.append((node.right, depth + 1))

		return max_depth

	# Exercise 4

	def is_valid(self):
		valid = True

		# Iterative DFS (stack)
		temp_nodes = [self]
		while temp_nodes:
			# Get node
			node = temp_nodes.pop()

			# Validate node
			if not node:
				continue

			# Update valid
			valid &= (node.left.value <= node.value) if node.left else True
			valid &= (node.value <= node.right.value) if node.right else True

			# Push child nodes
			if node.left:
				temp_nodes.append(node.left)
			if node.right:
				temp_nodes.append(node.right)

		return valid

	# Traverse with prefix (meant to work with strings)

	def traverse_inorder_with_prefix(self, prefix=""):
		result = []

		# Loop
		temp_nodes = []
		node: BinaryTreeNode = self
		while node or temp_nodes:
			# Handle left side
			while node:
				temp_nodes.append(node)

				# Check if left side can have prefix
				if node.value < prefix:
					# If the node is less than prefix, then
					# all nodes in the left subtree will be less then prefix
					break

				# Go to right
				node = node.left

			# Get next temporary node
			node = temp_nodes.pop()

			# Check if value contains prefix
			if node.value.startswith(prefix):
				result.append(node.value)

				# Loop from right subtree
				node = node.right
			elif node.value < prefix:
				# Bigger nodes can still have prefix
				node = node.right
			else:
				# All nodes in the right subtree can't have prefix
				node = None

		return result

# Tree class

class BinarySearchTree:
	def __init__(self) -> None:
		self.root = None

	# Root functions

	def set_root(self, node: BinaryTreeNode):
		self.root = node
		node.parent = None

	# Initialization

	def init_empty(self):
		self.root = None

	def init_array_balanced(self, node_values: list[int]):
		self.root = None
		self.insert_sorted_values_array(sorted(node_values), 0, len(node_values) - 1)

	# Insert functions

	def insert_node(self, node: BinaryTreeNode):
		# Validate node not under root
		if self.search_exact_node(node):
			return

		# If no root, set node as root
		if not self.root:
			self.set_root(node)
			return

		# Find the place to insert node
		temp_node = None
		next_temp_node = self.root
		while next_temp_node:
			# Set current temp node
			temp_node = next_temp_node

			# Find next temp node
			if is_left(temp_node.value, node.value):
				next_temp_node = temp_node.left
			else:
				next_temp_node = temp_node.right

		# Insert node
		if is_left(temp_node.value, node.value):
			temp_node.set_left(node)
		else:
			temp_node.set_right(node)

	def insert_node_with_value(self, value: NodeValueType):
		node = BinaryTreeNode(value)
		self.insert_node(node)

	# Swap functions

	def swap_node(self, node1: BinaryTreeNode, node2: BinaryTreeNode):
		# Swap node with successor
		node1.parent, node2.parent = node2.parent, node1.parent
		node1.left, node2.left = node2.left, node1.left
		node1.right, node2.right = node2.right, node1.right
		if node1.parent == node1:
			node1.parent = node2
		if node2.parent == node2:
			node2.parent = node1

		if node1.left == node1:
			node1.left = node2
		if node1.right == node1:
			node1.right = node2
		if node2.left == node2:
			node2.left = node1
		if node2.right == node2:
			node2.right = node1

		# Root update
		if self.root == node1:
			self.set_root(node2)
		elif self.root == node2:
			self.set_root(node1)

		# Set connected node's properties
		if node1.parent and node1.parent != node2:
			node1.parent.set_child(node1)
		if node1.left:
			node1.set_left(node1.left)
		if node1.right:
			node1.set_right(node1.right)

		if node2.parent and node2.parent != node1:
			node2.parent.set_child(node2)
		if node2.left:
			node2.set_left(node2.left)
		if node2.right:
			node2.set_right(node2.right)

	# Delete functions

	def delete_node(self, node: BinaryTreeNode):
		# print(f"del {node.value}")

		# Find the node's in-order successor
		# https://www.geeksforgeeks.org/deletion-in-binary-search-tree/
		node_successor = None
		if node.left:
			# In-order predecessor
			node_successor = self.find_max_node(node.left)
		elif node.right:
			# In-order successor
			node_successor = self.find_min_node(node.right)

		# Replace the node with the successor
		if node_successor:
			# print(f"Swap {node.value} with {node_successor.value}")

			self.swap_node(node, node_successor)

			# self.display()

			# Delete swapped node
			self.delete_node(node)

		# Remove node
		if node.parent:
			node.parent.remove_child(node)
		node.parent = None
		node.left = None
		node.right = None

	def delete_a_node_by_value(self, value: NodeValueType):
		# Get a node with same value
		node = self.search_node_with_value(value)

		# Remove node if found
		if node:
			self.delete_node(node)

	# Search functions

	def find_max_node(self, root=None):
		# Get the right-most node
		temp_node = None
		next_temp_node = root or self.root
		while next_temp_node:
			temp_node = next_temp_node
			next_temp_node = temp_node.right

		# Return node
		return temp_node

	def find_min_node(self, root=None):
		# Get the left-most node
		temp_node = None
		next_temp_node = root or self.root
		while next_temp_node:
			temp_node = next_temp_node
			next_temp_node = temp_node.left

		# Return node
		return temp_node

	def find_max_value(self):
		node = self.find_max_node()
		if node:
			return node.value
		else:
			return
	
	def find_min_value(self):
		node = self.find_min_node()
		if node:
			return node.value
		else:
			return

	def find_max_node_with_upperlimit(self, limit: NodeValueType, root=None):
		result_node = None

		# Get the right-most node <= limit
		temp_node = None
		next_temp_node = root or self.root
		while next_temp_node:
			temp_node = next_temp_node
			if temp_node.value <= limit:
				result_node = temp_node

			if temp_node.value <= limit:
				next_temp_node = temp_node.right
			else:
				next_temp_node = temp_node.left

		# Return node
		return result_node

	def find_min_node_with_lowerlimit(self, limit: NodeValueType, root=None):
		result_node = None

		# Get the left-most node >= limit
		temp_node = None
		next_temp_node = root or self.root
		while next_temp_node:
			temp_node = next_temp_node
			if temp_node.value >= limit:
				result_node = temp_node

			if temp_node.value >= limit:
				next_temp_node = temp_node.left
			else:
				next_temp_node = temp_node.right

		# Return node
		return result_node

	# This function is meant to work with strings
	def find_first_node_with_prefix(self, prefix: NodeValueType, root=None):
		result_node = None

		# Get the first node with prefix
		temp_node = None
		next_temp_node = root or self.root
		while next_temp_node:
			temp_node = next_temp_node

			# Prefix check
			if temp_node.value.startswith(prefix):
				result_node = temp_node
				break

			# Traverse
			if temp_node.value >= prefix:
				next_temp_node = temp_node.left
			else:
				next_temp_node = temp_node.right

		# Return node
		return result_node

	def search_node_with_value(self, key: NodeValueType, root=None):
		temp_node = None
		next_temp_node = root or self.root
		while next_temp_node:
			temp_node = next_temp_node
			if temp_node.value == key:
				return temp_node
			if is_left(temp_node.value, key):
				next_temp_node = temp_node.left
			else:
				next_temp_node = temp_node.right
		return

	def search_exact_node(self, node: BinaryTreeNode, root=None):
		temp_node = None
		next_temp_node = root or self.root
		while next_temp_node:
			temp_node = next_temp_node
			if temp_node == node:
				return temp_node
			if is_left(temp_node.value, node.value):
				next_temp_node = temp_node.left
			else:
				next_temp_node = temp_node.right
		return

	# Display functions

	def display(self):
		if self.root:
			self.root.display_subtree()
		else:
			print(None)

	# Traverse

	def traverse_inorder(self):
		if self.root:
			return self.root.traverse_inorder()
		else:
			return None

	# Depth

	def max_depth(self):
		if self.root:
			return self.root.get_depth()
		else:
			return None

	# Valid

	def is_valid(self):
		if self.root:
			return self.root.is_valid()
		else:
			return None

	# Exercise 5

	def insert_sorted_values_array(self, values: list[NodeValueType], left_bound: int, right_bound: int):
		if not left_bound <= right_bound:
			return

		middle = left_bound + (right_bound - left_bound) // 2
		self.insert_node_with_value(values[middle])
		self.insert_sorted_values_array(values, left_bound, middle - 1)
		self.insert_sorted_values_array(values, middle + 1, right_bound)

# Example test

if __name__ == "__main__":
	# Initialize tree
	bst = BinarySearchTree()

	# Create nodes and build tree
	node_values = [5, 0, 1, 2, 2, 3, 4]
	for value in node_values:
		bst.insert_node_with_value(value)

	# Display tree information
	bst.display()
	print(f"Min: {bst.find_min_value()}")
	print(f"Max: {bst.find_max_value()}")

	# Delete nodes
	delete_values = [0]
	for value in delete_values:
		bst.delete_a_node_by_value(value)
	bst.display()
	print(f"Min: {bst.find_min_value()}")
	print(f"Max: {bst.find_max_value()}")

	# Note: deleting nodes via swapping the 'inorder successor' might
	# violate the is_left() condition for duplicate values

	### Other exercises

	# Inorder
	print(f"Inorder: {bst.traverse_inorder()}")

	# Max depth
	print(f"Depth: {bst.max_depth()}")

	# Check BST
	print(f"Valid: {bst.is_valid()}")

	# Array to balanced BST
	bst.init_array_balanced([1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
	bst.display()
	print(f"Inorder: {bst.traverse_inorder()}")
	print(f"Depth: {bst.max_depth()}")
	print(f"Valid: {bst.is_valid()}")
