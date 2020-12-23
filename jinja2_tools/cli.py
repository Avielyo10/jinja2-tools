import click
import json
import yaml

from jinja2 import Template
from jinja2 import exceptions
from colors import red, green


def print_verbose(title, content):
    separator = green(f'{"-" * 10}')
    print(separator, title, separator)
    print(green(content))


@click.group()
def main():
    pass


@main.command()
@click.option('--data', '-d', type=click.Path(exists=True))
@click.option('--template', '-t', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True)
@click.option('--trim-blocks', '-tb', default=True, is_flag=True)
@click.option('--lstrip-blocks', '-lb', default=True, is_flag=True)
def render(data, template, verbose, trim_blocks, lstrip_blocks):
    if data is not None:
        with open(data, 'r') as input_data_file:
            data = yaml.load(input_data_file.read(), Loader=yaml.FullLoader)
            if verbose:
                print_verbose('[Data]', json.dumps(data, indent=2))

    if template is not None:
        with open(template, 'r') as input_template_file:
            template_file = input_template_file.read()
            tm = Template(template_file,
                          trim_blocks=trim_blocks, lstrip_blocks=lstrip_blocks)
            if verbose:
                print_verbose('[Template]', template_file)
            try:
                if data is not None:
                    print(tm.render(data))
                else:
                    print(tm.render())
            except exceptions.UndefinedError as err:
                print(red('[ERROR]'), err.message)
