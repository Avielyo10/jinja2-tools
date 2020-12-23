import click
import json
import yaml

from jinja2 import Template, exceptions
from colors import red, green


def print_verbose(data):
    if data['verbose']:
        separator = green(f'{"-" * 10}')
        print(separator, data['title'], separator)
        print(green(data['content']), "\n")


@click.group()
def main():
    pass


@main.command()
@click.option('--data', '-d', type=click.Path(exists=True))
@click.option('--template', '-t', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True)
@click.option('--trim-blocks', '-tb', default=True, is_flag=True)
@click.option('--lstrip-blocks', '-lb', default=True, is_flag=True)
@click.option('--output', '-o', type=click.Path())
def render(data, template, verbose, trim_blocks, lstrip_blocks, output):
    if data is not None:
        with open(data, 'r') as input_data_file:
            data = yaml.load(input_data_file.read(), Loader=yaml.FullLoader)
            print_verbose({'title': '[Data]', 'content': json.dumps(
                data, indent=2), 'verbose': verbose})

    if template is not None:
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
