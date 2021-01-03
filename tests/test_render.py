import os
import sys
import requests
import shutil
import yaml

from filecmp import dircmp
from io import StringIO

from click.testing import CliRunner
from jinja2_tools.cli import main as jinja

TEMPLATE_URL = 'https://raw.githubusercontent.com/Avielyo10/jinja2-tools/master/examples/templates/template.yaml'
DATA_URL = 'https://raw.githubusercontent.com/Avielyo10/jinja2-tools/master/examples/data/data.yaml'
EXTRA_VARS = 'access_lists={\"al-hq-in\": [{\"action\": \"remark\", \"text\": \"Allow traffic from hq to local office\"}, {\"action\": \"permit\", \"src\": \"10.0.0.0/22\", \"dst\": \"10.100.0.0/24\"}]}'

DEFAULT_MSG = """(1)
ip access-list extended al-hq-in
(2)
    (3)    remark Allow traffic from hq to local office
    (4)(2)
    (3)    permit 10.0.0.0/22 10.100.0.0/24
    (5)(6)
(7)
hello jinja!
# All ACLs have been generated
"""

MSG_WITH_LB_TB = """(1)
ip access-list extended al-hq-in
  (2)
    (3)
    remark Allow traffic from hq to local office
    (4)
  (2)
    (3)
    permit 10.0.0.0/22 10.100.0.0/24
    (5)
  (6)
(7)
hello jinja!
# All ACLs have been generated
"""

DIR_COMPARISONS="""diff test/ examples/
Common subdirectories : ['config', 'data', 'templates']

diff test/config examples/config
Identical files : ['example.ini', 'example.properties']

diff test/data examples/data
Identical files : ['data.json', 'data.yaml']

diff test/templates examples/templates
Differing files : ['lookup.yaml', 'template.yaml']
"""
os.environ['SHELL'] = '/usr/bin/zsh'


def test_simple_render():
    runner = CliRunner()
    yaml_result = runner.invoke(
        jinja, ['render', '-d', 'examples/data/data.yaml', '-t', 'examples/templates/template.yaml'])
    assert yaml_result.exit_code == 0
    assert yaml_result.output == DEFAULT_MSG

    json_result = runner.invoke(
        jinja, ['render', '-d', 'examples/data/data.json', '-t', 'examples/templates/template.yaml'])
    assert json_result.output == yaml_result.output


def test_simple_render_with_tb_lb():
    runner = CliRunner()
    yaml_result = runner.invoke(
        jinja, ['render', '-lb', '-tb', '-d', 'examples/data/data.yaml', '-t', 'examples/templates/template.yaml'])
    assert yaml_result.exit_code == 0
    assert yaml_result.output == MSG_WITH_LB_TB

    json_result = runner.invoke(
        jinja, ['render', '-lb', '-tb', '-d', 'examples/data/data.json', '-t', 'examples/templates/template.yaml'])
    assert json_result.output == yaml_result.output


def test_render_with_url():
    runner = CliRunner()
    result = runner.invoke(
        jinja, ['render', '-d', DATA_URL, '-t', TEMPLATE_URL])
    assert result.exit_code == 0
    assert result.output == DEFAULT_MSG


def test_render_with_stdin_data():
    runner = CliRunner()
    result = runner.invoke(
        jinja, ['render', '-d', '-', '-t', TEMPLATE_URL], input=requests.get(DATA_URL).text)
    assert result.exit_code == 0
    assert result.output == DEFAULT_MSG


def test_render_with_stdin_template():
    runner = CliRunner()
    result = runner.invoke(
        jinja, ['render', '-d', DATA_URL, '-t', '-'], input=requests.get(TEMPLATE_URL).text)
    assert result.exit_code == 0
    assert result.output == DEFAULT_MSG


def test_render_with_extra_vars():
    runner = CliRunner()
    result = runner.invoke(
        jinja, ['render', '-d', 'examples/data/data.yaml', '-t', 'examples/templates/template.yaml', '-e', EXTRA_VARS])

    assert result.exit_code == 0
    assert result.output == DEFAULT_MSG


def test_render_with_extra_vars_override():
    runner = CliRunner()
    result = runner.invoke(
        jinja, ['render', '-d', 'examples/data/data.yaml', '-t', 'examples/templates/template.yaml', '-e', EXTRA_VARS, '-e', 'message=world'])

    assert result.exit_code == 0
    assert 'hello world!' in result.output


def test_render_with_directory():
    runner = CliRunner()
    test_dir = 'test/'
    result = runner.invoke(
        jinja, ['render', '-d', 'examples/data/data.yaml', '-t', 'examples/', '-o', test_dir])

    assert result.exit_code == 0
    ### report_full_closure() just print to stdout, so we capture it
    s_io = StringIO()
    sys.stdout = s_io
    dircmp(test_dir, 'examples/').report_full_closure()
    sys.stdout = sys.__stdout__
    s_io.seek(0, os.SEEK_SET)
    assert s_io.read() == DIR_COMPARISONS
    try:
        shutil.rmtree(test_dir)
    except FileNotFoundError as err:
        print(err.strerror)


def test_invalid_input():
    runner = CliRunner()
    yaml_result = runner.invoke(
        jinja, ['render', '-d', '-', '-t', '-'])
    assert yaml_result.exit_code == 127


def test_invalid_data_type():
    runner = CliRunner()
    test_dir = 'test/'
    result = runner.invoke(
        jinja, ['render', '-d', 'examples/', '-t', 'examples/', '-o', test_dir])

    assert result.exit_code == 128
    try:
        shutil.rmtree(test_dir)
    except FileNotFoundError:
        pass


def test_render_with_bad_url():
    runner = CliRunner()
    result = runner.invoke(
        jinja, ['render', '-d', DATA_URL+'/bla', '-t', TEMPLATE_URL])
    assert result.exit_code != 0

def test_lookup():
    runner = CliRunner()
    test_dir = 'test/'
    result = runner.invoke(
        jinja, ['render', '-d', 'examples/data/data.yaml', '-t', 'examples/', '-o', test_dir])

    assert result.exit_code == 0

    with open('test/templates/lookup.yaml', 'r') as f:
        out = yaml.full_load(f)
    lookup = out['lookup']
    
    assert lookup[0] == '/usr/bin/zsh'
    assert lookup[1] == 'gertrude'
    assert lookup[2] == ['john', 'passwd']
    assert lookup[3] == 'robert'
    assert lookup[4] == ['robert', 'somerandompassword']
    try:
        shutil.rmtree(test_dir)
    except FileNotFoundError as err:
        print(err.strerror)