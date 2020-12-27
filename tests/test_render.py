import os
import requests
import shutil

from click.testing import CliRunner
from jinja2_tools.cli import main as jinja

TEMPLATE_URL = 'https://raw.githubusercontent.com/Avielyo10/jinja2-tools/master/examples/template.sh'
DATA_URL = 'https://raw.githubusercontent.com/Avielyo10/jinja2-tools/master/examples/data.yaml'
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


def test_simple_render():
    runner = CliRunner()
    yaml_result = runner.invoke(
        jinja, ['render', '-d', 'examples/data.yaml', '-t', 'examples/template.sh'])
    assert yaml_result.exit_code == 0
    assert yaml_result.output == DEFAULT_MSG

    json_result = runner.invoke(
        jinja, ['render', '-d', 'examples/data.json', '-t', 'examples/template.sh'])
    assert json_result.output == yaml_result.output


def test_simple_render_with_tb_lb():
    runner = CliRunner()
    yaml_result = runner.invoke(
        jinja, ['render', '-lb', '-tb', '-d', 'examples/data.yaml', '-t', 'examples/template.sh'])
    assert yaml_result.exit_code == 0
    assert yaml_result.output == MSG_WITH_LB_TB

    json_result = runner.invoke(
        jinja, ['render', '-lb', '-tb', '-d', 'examples/data.json', '-t', 'examples/template.sh'])
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
        jinja, ['render', '-d', 'examples/data.yaml', '-t', 'examples/template.sh', '-e', EXTRA_VARS])

    assert result.exit_code == 0
    assert result.output == DEFAULT_MSG


def test_render_with_extra_vars_override():
    runner = CliRunner()
    result = runner.invoke(
        jinja, ['render', '-d', 'examples/data.yaml', '-t', 'examples/template.sh', '-e', EXTRA_VARS, '-e', 'message=world'])

    assert result.exit_code == 0
    assert 'hello world!' in result.output


def test_render_with_directory():
    runner = CliRunner()
    test_dir = 'test/'
    result = runner.invoke(
        jinja, ['render', '-d', 'examples/data.yaml', '-t', 'examples/', '-o', test_dir])

    assert result.exit_code == 0
    assert len(os.listdir(test_dir)) == 3
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
    except OSError:
        pass
