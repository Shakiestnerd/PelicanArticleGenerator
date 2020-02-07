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
        self.filename = f'{self.slug}.{self.output_type}'
        if os.path.isdir('./content/' + self.category):
            self.base_folder = './content/' + self.category
        self.full_file = os.path.join(self.base_folder, self.filename)
        with open(self.full_file, "w") as out_file:
            out_file.writelines(body)
        print("File created: " + self.full_file)

    def format_markdown(self):
        content = []
        content.append('---\n')
        content.append(f'Title: {self.title}\n' )
        content.append(f'Date: {self.date}\n')
        content.append(f'Category: {self.category}\n')
        content.append(f'Tags: {self.tags}\n')
        content.append(f'Author: {self.author}\n')
        content.append(f'Status: {self.status}\n')
        if len(self.summary) > 0:
            content.append(f'Summary: {self.summary}\n')
        content.append('---\n\n')
        if self.is_recipe:
            content.append('Insert description of recipe here\n\n')
            content.append('![_Image Title_][1]\n\n')
            content.append('## Ingredients\n\n')
            content.append('List all the ingredients\n\n')
            content.append('## Instructions\n\n')
            content.append('Write detailed instructions here.\n\n')
            content.append('## Remarks\n\n')
            content.append('Add closing remarks here\n\n')
            content.append('[1]: ../images/_filename_ "_Image Description_"\n')
        else:
            content.append('Insert article here.\n')
        return content

    def format_rst(self):
        pass
