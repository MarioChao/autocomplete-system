# Command line interface

# Import

from binary_tree.avl_tree import AvlTree
from binary_tree.binary_search_tree import BinarySearchTree

# Variables

commands = {
	"1": "Insert a word",
	"2": "Search for a word",
	"3": "Autocomplete a word",
	"4": "Show all words",
	"0": "Show commands",
	"-1": "Exit",
}

word_tree = AvlTree()

# Helper functions

def __input_and_confirm(input_message) -> tuple[bool, str]:
	# Input
	# print(input_message)
	value = input(f"{input_message} > ")

	# Confirmation input
	while True:
		confirm = input(f"Are you sure about '{value}' (y/n)? ")
		if confirm in ("y", "n"):
			break

	if confirm == "y":
		return True, value
	else:
		return False, None

# Local functions

def show_commands():
	print("Command options:")
	for key, description in commands.items():
		print(f"{key}. {description}")

def input_command():
	print("Enter command")
	command = input("> ")

	# Validate command
	if not is_command_available(command):
		print("Not a valid command!")
		return None

	# Return
	return command

def is_command_available(command):
	return command in commands.keys()

def process_command(command):
	assert is_command_available(command)

	# Commands
	match command:
		case "1":
			# Input word
			success, word = __input_and_confirm("Enter a word to insert")
			if not success:
				return

			# Lowercase the word
			word = word.lower()

			# Validate new word
			if word_tree.search_node_with_value(word):
				print(f"Word already in the autocomplete system!")
				return

			# Insert word
			word_tree.insert_node_with_value(word)
			print(f"Word '{word}' has been inserted.")
		case "2":
			# Input word
			success, word = __input_and_confirm("Enter a word to search")
			if not success:
				return

			# Lowercase the word
			word = word.lower()

			# Search
			if word_tree.search_node_with_value(word):
				print(f"200 Found!")
			else:
				print(f"404 word not found")
		case "3":
			# Input prefix
			success, prefix = __input_and_confirm("Enter a prefix to autocomplete")
			if not success:
				return

			# Lowercase the prefix
			prefix = prefix.lower()

			# Find first word with prefix
			node = word_tree.find_first_node_with_prefix(prefix)

			# Suggest all words with prefix
			nodes = []
			if node:
				nodes = node.traverse_inorder_with_prefix(prefix)
			print(f"Suggestions: {nodes}")
		case "4":
			print(f"All words in the system:")
			nodes = word_tree.traverse_inorder()
			print(f"{nodes}")
		case "0":
			show_commands()
		case "-1":
			return -1
