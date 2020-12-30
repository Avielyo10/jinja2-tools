"""
setup.py for using pip
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="jinja2-tools",
    version="1.0.6",
    author="Aviel Yosef",
    author_email="Avielyo10@gmail.com",
    description="Use Jinja2 templates via cli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Avielyo10/jinja2-tools.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'Click',
        'ansicolors',
        'PyYAML',
        'Jinja2',
        'requests',
        'validators'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    entry_points='''
        [console_scripts]
        jinja=jinja2_tools.cli:main
    ''',
)
