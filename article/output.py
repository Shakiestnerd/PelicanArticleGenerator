import os


class Output:
    def __init__(self):
        super().__init__()
        self.title = ""
        self.date = ""
        self.tags = ""
        self.slug = ""
        self.category = ""
        self.status = ""
        self.author = ""
        self.output_type = "md"
        self.summary = ""
        self.is_recipe = False
        self.filename = ""
        self.base_folder = ""
        self.full_file = ""

    def save_article(self):
        if self.output_type == "md":
            body = self.format_markdown()
        else:
            body = self.format_rst()
        if os.path.isdir(self.base_folder):
            with open(self.full_file, "w") as out_file:
                out_file.writelines(body)
            print("File created: " + self.full_file)
        else:
            print(f"Folder {self.base_folder} not found.")

    def format_markdown(self):
        content = ["---\n", f"Title: {self.title}\n", f"Date: {self.date}\n",
                   f"Category: {self.category}\n", f"Tags: {self.tags}\n"]
        if "," in self.author:
            author_title = "Authors:"
        else:
            author_title = "Author:"
        content.append(f"{author_title} {self.author}\n")
        content.append(f"Status: {self.status}\n")
        if self.summary:
            content.append(f"Summary: {self.summary}\n")
        content.append("---\n\n")
        if self.is_recipe:
            content.append("Insert description of recipe here\n\n")
            content.append("![_Image Title_][1]\n\n")
            content.append("## Ingredients\n\n")
            content.append("List all the ingredients\n\n")
            content.append("## Instructions\n\n")
            content.append("Write detailed instructions here.\n\n")
            content.append("## Remarks\n\n")
            content.append("Add closing remarks here\n\n")
            content.append('[1]: ../images/_filename_ "_Image Description_"\n')
        else:
            content.append("Insert markdown article here.\n")
        return content

    def format_rst(self):
        content = [f"{self.title}\n", "=" * len(self.title), f"\n:Date: {self.date}\n",
                   f":Category: {self.category}\n", f":Tags: {self.tags}\n",
                   f":Author: {self.author}\n", f":Status: {self.status}\n\n"]
        if self.is_recipe:
            content.append("Insert description of recipe here\n\n")
            content.append(".. image:: ../images/_filename_\n\n")
            content.append("Ingredients\n")
            content.append("-----------\n\n")
            content.append("List all the ingredients\n\n")
            content.append("Instructions\n")
            content.append("------------\n\n")
            content.append("Write detailed instructions here.\n\n")
            content.append("Remarks\n")
            content.append("-------\n\n")
            content.append("Add closing remarks here\n\n")
        else:
            content.append("Insert restructured text article here.\n")
        return content
