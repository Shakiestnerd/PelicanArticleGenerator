"""Save and retrieve the user options from articles.ini."""
import configparser
import os


class UserOptions:
    """Read the user last selections from articles.ini"""

    def __init__(self):
        self.init_file = "articles.ini"
        self.base_folder = ""
        self.author = ""
        self.categories = []
        self.favorite_tags = []
        self.default_type = "md"

        if os.access(self.init_file, os.R_OK):
            self.load_config()

    def load_config(self):
        """Load the configuration file
        """
        config = configparser.ConfigParser()
        try:
            config.read(self.init_file)
            self.base_folder = config["src"]["base_folder"]
            self.author = config["src"]["author"]
            self.categories = config["src"]["categories"].split(",")
            self.favorite_tags = config["src"]["tags"].split(",")
            self.default_type = config["src"]["default_type"]
        except KeyError:
            return

    def save_config(self):
        """Save the configuration data.
        """
        config = configparser.ConfigParser()
        config_file = open(self.init_file, "w")
        # config.read('articles.ini')
        config.add_section("src")
        config.set("src", "base_folder", self.base_folder)
        config.set("src", "author", self.author)
        config.set("src", "tags", self.favorite_tags)
        config.set("src", "categories", "|".join(self.categories))
        config.set("src", "default_type", self.default_type)
        config.write(config_file)
        config_file.close()


if __name__ == "__main__":
    opt = UserOptions()
    opt.save_config()
