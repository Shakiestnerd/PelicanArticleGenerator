"""Save and retrieve the user options."""
import configparser
import os


class UserOptions:
    """Read the user last selections from articles.ini"""

    def __init__(self):
        self.init_file = "articles.ini"
        self.base_folder = ""
        self.author = ""
        self.categories = []
        self.favorite_tags = ""
        self.default_type = "md"

        if os.access(self.init_file, os.R_OK):
            self.load_config()

    def load_config(self):
        """Load the configuration file
        """
        config = configparser.ConfigParser()
        try:
            config.read(self.init_file)
            self.base_folder = config["article"]["base_folder"]
            self.author = config["article"]["author"]
            self.categories = config["article"]["categories"]
            self.favorite_tags = config["article"]["tags"]
            self.default_type = config["article"]["default_type"]
        except KeyError:
            return

    def save_config(self):
        """Save the configuration data.
        """
        config = configparser.ConfigParser()
        config_file = open(self.init_file, "w")
        # config.read('articles.ini')
        config.add_section("article")
        config.set("article", "base_folder", self.base_folder)
        config.set("article", "author", self.author)
        config.set("article", "tags", self.favorite_tags)
        for cat in self.categories:
            config.set("article", "categories", cat)
        config.set("article", "default_type", self.default_type)
        config.write(config_file)
        config_file.close()


if __name__ == "__main__":
    opt = UserOptions()
    opt.save_config()
