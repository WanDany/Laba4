def get_file_content(filename):
    """Read content from a specified file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None

def format_content(content, lines_per_page, left_margin):
    """Format content with specified lines per page and left margin."""
    formatted_content = ""
    page_line_count = 0

    for line in content:
        # Add left margin and line content
        formatted_content += " " * left_margin + line

        page_line_count += 1
        if page_line_count >= lines_per_page:
            formatted_content += "\n--- Page Break ---\n"
            page_line_count = 0

    return formatted_content

def save_to_file(content, output_filename):
    """Save content to a specified output file."""
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Content successfully saved to '{output_filename}'")
    except IOError as e:
        print(f"Failed to write to file '{output_filename}': {e}")

def main():
    filename = input("Enter the name of the text file to format and print: ")
    content = get_file_content(filename)
    if content is None:
        return

    try:
        lines_per_page = int(input("Enter the number of lines per page: "))
        left_margin = int(input("Enter the number of spaces for left margin: "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    formatted_content = format_content(content, lines_per_page, left_margin)

    print("Choose output option:")
    print("1. Print to screen")
    print("2. Save to another file")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        print("\nDisplaying formatted content on screen:\n")
        print(formatted_content)
    elif choice == '2':
        output_filename = input("Enter the name of the output file: ")
        save_to_file(formatted_content, output_filename)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
