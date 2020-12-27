import click
import os

from .objects import Data, Template, ExtraVar
from .exceptions import InvalidInput
from .validators import validate_is_dir
from .util import output_template


@click.group()
@click.version_option()
def main():
    pass


@main.command()
@click.option('--data', '-d', help="PATH to YAML or JSON data file, URL or '-' for stdin.")
@click.option('--template', '-t', help="PATH to directory or to"
              " any file that uses Jinja, URL or '-' for stdin.")
@click.option('--verbose', '-v', is_flag=True)
@click.option('--no-trim-blocks', '-tb', default=True, is_flag=True, help='Disable trim blocks.')
@click.option('--no-lstrip-blocks', '-lb', default=True, is_flag=True, help='Disable lstrip blocks.')
@click.option('--output', '-o', type=click.Path(), help='PATH for output, stdout by default.')
@click.option('--extra-var', '-e', multiple=True, help="key value pair separated by '='. "
              "'value' will be treated as JSON or as a string in case of JSON decoding error. "
              "This will take precedence over 'data'.")
def render(data, template, verbose, no_trim_blocks, no_lstrip_blocks, output, extra_var):
    if data == '-' and template == '-':
        raise InvalidInput()

    if data is not None:
        data = Data(data, verbose).get_data()

    if extra_var is not None:
        extra_var = ExtraVar(extra_var, verbose).get_extra_vars()
        if data is not None:
            data.update(extra_var)
        else:
            data = extra_var

    if template is not None:
        if validate_is_dir(template):
            for root, dirs, files in os.walk(template):
                # Skip hidden directories
                files = [file for file in files if not file[0] == '.']
                dirs[:] = [dir for dir in dirs if not dir[0] == '.']

                for file in files:
                    template_path = os.path.join(root, file)
                    out = Template(template_path, verbose, data, no_trim_blocks,
                                   no_lstrip_blocks).get_rendered_template()
                    output_template(
                        content=out, output_path=output, dir=os.path.relpath(template_path, template))
        else:
            out = Template(template, verbose, data, no_trim_blocks,
                           no_lstrip_blocks).get_rendered_template()
            output_template(out, output)
