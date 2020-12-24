# Jinja2 tools

Use Jinja2 templates via cli

## Install

```
$ pip install jinja2-tools
```

## Usage

```
Usage: jinja render [OPTIONS]

Options:
  -d, --data TEXT          PATH to YAML or JSON data file, URL or '-' for
                           stdin

  -t, --template TEXT      PATH to any file that uses Jinja, URL or '-' for
                           stdin

  -v, --verbose
  -tb, --no-trim-blocks    Disable trim blocks
  -lb, --no-lstrip-blocks  Disable lstrip blocks
  -o, --output PATH        PATH for output, stdout by default
  --help                   Show this message and exit.
```

## Whitespace Control

`trim_blocks` and `lstrip_blocks` are used by default, to disable them use `-tb` or `-lb` respectively.

## Examples

* Use path from the filesystem for data & template:
  ```
  ➜  jinja2-tools git:(master) jinja render -d examples/data.yaml -t examples/template.sh
  (1)
  ip access-list extended al-hq-in
  (2)
      (3)    remark Allow traffic from hq to local office
      (4)(2)
      (3)    permit 10.0.0.0/22 10.100.0.0/24
      (5)(6)
  (7)

  # All ACLs have been generated
  ```

* Use stdin for data & URL for template, also disable trim blocks & lstrip blocks:
  ```
  ➜  jinja2-tools git:(master) jinja render -d - -t https://raw.githubusercontent.com/Avielyo10/jinja2-tools/master/examples/template.sh -lb -tb < examples/data.yaml
  (1)
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

  # All ACLs have been generated
  ```

* Verbose:
  ```
  ➜  jinja2-tools git:(master) jinja render -d examples/data.yaml -t examples/template.sh -v     
  ---------- [Data] ----------
  {
    "access_lists": {
      "al-hq-in": [
        {
          "action": "remark",
          "text": "Allow traffic from hq to local office"
        },
        {
          "action": "permit",
          "src": "10.0.0.0/22",
          "dst": "10.100.0.0/24"
        }
      ]
    }
  }

  ---------- [Template] ----------
  {% for acl, acl_lines in access_lists.items() %}(1)
  ip access-list extended {{ acl }}
    {% for line in acl_lines %}(2)
      (3){% if line.action == "remark" %}
      remark {{ line.text }}
      (4){% elif line.action == "permit" %}
      permit {{ line.src }} {{ line.dst }}
      (5){% endif %}
    {% endfor %}(6)
  {% endfor %}(7)

  # All ACLs have been generated

  (1)
  ip access-list extended al-hq-in
  (2)
      (3)    remark Allow traffic from hq to local office
      (4)(2)
      (3)    permit 10.0.0.0/22 10.100.0.0/24
      (5)(6)
  (7)

  # All ACLs have been generated
  ```