# Imports

import cli

# Main function

if __name__ == "__main__":
	# Intro
	print()
	print(f"{"[ Autocomplete System ]":-^50}")

	# Show commands
	print()
	cli.show_commands()

	# Interactive
	while True:
		# Newline
		print()

		# Input
		command = cli.input_command()
		if not command:
			continue

		# Process
		result = cli.process_command(command)
		if result == -1:
			break

	# Exit
	print()
	print("Thank you for using the system. Goodbye!")
	print()
