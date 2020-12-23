import click
import json
import requests
import validators
import yaml

from colors import red, green
from jinja2 import Template, exceptions


def print_verbose(data):
    if data['verbose']:
        separator = green(f'{"-" * 10}')
        print(separator, data['title'], separator)
        print(green(data['content']), "\n")


@click.group()
def main():
    pass


@main.command()
@click.option('--stream', '-s', type=click.File('r'))
@click.option('--data', '-d')
@click.option('--template', '-t')
@click.option('--verbose', '-v', is_flag=True)
@click.option('--trim-blocks', '-tb', default=True, is_flag=True)
@click.option('--lstrip-blocks', '-lb', default=True, is_flag=True)
@click.option('--output', '-o', type=click.Path())
def render(stream, data, template, verbose, trim_blocks, lstrip_blocks, output):
    if data is not None:
        if validators.url(data):
            r = requests.get(data)
            if r.status_code < 400:
                data = yaml.load(r.text, Loader=yaml.FullLoader)
                print_verbose({'title': '[Data]', 'content': json.dumps(
                    data, indent=2), 'verbose': verbose})
        else:
            with open(data, 'r') as input_data_file:
                data = yaml.load(input_data_file.read(),
                                 Loader=yaml.FullLoader)
                print_verbose({'title': '[Data]', 'content': json.dumps(
                    data, indent=2), 'verbose': verbose})

    if stream is not None and data is None:
        data = yaml.load(stream.read(), Loader=yaml.FullLoader)
        print_verbose({'title': '[Data]', 'content': json.dumps(
            data, indent=2), 'verbose': verbose})

    if template is not None:
        if validators.url(template):
            r = requests.get(template)
            if r.status_code < 400:
                template_file = r.text
                tm = Template(template_file,
                              trim_blocks=trim_blocks, lstrip_blocks=lstrip_blocks)
                print_verbose(
                    {'title': '[Template]', 'content': template_file, 'verbose': verbose})
        else:
            with open(template, 'r') as input_template_file:
                template_file = input_template_file.read()
                tm = Template(template_file,
                              trim_blocks=trim_blocks, lstrip_blocks=lstrip_blocks)
                print_verbose(
                    {'title': '[Template]', 'content': template_file, 'verbose': verbose})

        try:
            if data is not None:
                out = tm.render(data)
            else:
                out = tm.render()

            if output is not None:
                with open(output, 'w+') as output_file:
                    output_file.write(out)
            else:
                print(out)
        except exceptions.UndefinedError as err:
            print(red('[ERROR]'), err.message)
