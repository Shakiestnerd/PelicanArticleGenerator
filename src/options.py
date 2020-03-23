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
        self.last_tags = []
        self.favorite_tags = []
        self.default_type = "md"

        # if os.access(self.init_file, os.R_OK):
        self.load_config()

    def load_config(self):
        """Load the configuration file
        """
        config = configparser.ConfigParser()
        try:
            config.read(self.init_file)
            print(config.sections())
            self.base_folder = config["default"]["base_folder"]
            self.author = config["default"]["author"]
            self.categories = config["default"]["categories"].split(",")
            self.last_tags = config["default"]["last_tags"].split(",")
            self.favorite_tags = config["default"]["tags"].split(",")
            self.default_type = config["default"]["default_type"]
        except KeyError:
            return

    def save_config(self):
        """Save the configuration data.
        """
        config = configparser.ConfigParser()

        # config.read('articles.ini')
        config.add_section("default")
        config.set("default", "base_folder", self.base_folder)
        config.set("default", "author", self.author)
        if type(self.last_tags) == str:
            config.set("default", "last_tags", self.last_tags)
        else:
            config.set("default", "last_tags", ",".join(self.last_tags))
        config.set("default", "tags", ",".join(self.favorite_tags))
        config.set("default", "categories", ",".join(self.categories))
        config.set("default", "default_type", self.default_type)
        with open(self.init_file, "w") as config_file:
            config.write(config_file)


if __name__ == "__main__":
    opt = UserOptions()
    opt.save_config()
