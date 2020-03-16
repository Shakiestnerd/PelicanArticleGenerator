from setuptools import setup, find_packages

setup(
    name="ArticleGenerater",
    version="0.1",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_required=["PySimpleGUI==4.16.0"],
    test_suite="tests",
    entry_points={"console_scripts": ["run=src.article:UI"]},
)

