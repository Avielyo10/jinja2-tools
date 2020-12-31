"""
jinja cli
"""

import os
import sys
import traceback
import click

from jinja2 import Environment, FileSystemLoader

from .exceptions import InvalidInput
from .objects import Data, Template, ExtraVar
from .util import output_template
from .validators import validate_is_dir


@click.group()
@click.version_option()
def main():
    """
    Main click group for future commands
    """
    pass


@main.command()
@click.option('--data', '-d', help="PATH to YAML or JSON data file, URL or '-' for stdin.")
@click.option('--template', '-t', help="PATH to directory or to"
              " any file that uses Jinja, URL or '-' for stdin.")
@click.option('--verbose', '-v', is_flag=True)
@click.option('--no-trim-blocks', '-tb', default=True, is_flag=True, help='Disable trim blocks.')
@click.option('--no-lstrip-blocks', '-lb', default=True, is_flag=True,
              help='Disable lstrip blocks.')
@click.option('--output', '-o', type=click.Path(), help='PATH for output, stdout by default.')
@click.option('--extra-var', '-e', multiple=True, help="key value pair separated by '='. "
              "'value' will be treated as JSON or as a string in case of JSON decoding error. "
              "This will take precedence over 'data'.")
def render(data, template, verbose, no_trim_blocks, no_lstrip_blocks, output, extra_var):
    """
    Render templates using Jinja2
    You can render a template (or a directory) from URL, PATH or stdin,
    using data from a URL, file or stdin.
    """
    if data == '-' and template == '-':
        try:
            raise InvalidInput()
        except:
            traceback.print_exc()
            sys.exit(127)

    if data is not None:
        data = Data(data, verbose).get_data()
    else:
        data = dict()

    if extra_var is not None:
        extra_var = ExtraVar(extra_var, verbose).get_extra_vars()
        data.update(extra_var)

    if template is not None:
        options = {'no_trim_blocks': no_trim_blocks,
                   'no_lstrip_blocks': no_lstrip_blocks}

        if validate_is_dir(template):
            env = Environment(loader=FileSystemLoader(template))
            for path in env.list_templates():
                template_path = os.path.join(template, path)
                out = Template(template_path, verbose, data,
                               options).get_rendered_template()
                output_template(
                    content=out, output_path=output,
                    relative_path=path)
        else:
            out = Template(template, verbose, data,
                           options).get_rendered_template()
            output_template(out, output)
