class MarkdownWriter:
    def __init__(self, content):
        self.content = content

    def write_to_file(self, filename="README.md"):
        with open(filename, "w") as f:
            f.write(self.content)
        print(f"{filename} generated successfully.")

    def get_markdown_file(self):
        return self.content.encode('utf-8')
