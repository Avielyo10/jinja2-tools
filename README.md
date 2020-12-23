# Jinja2 tools

Use Jinja2 templates via cli

## Usage

```
Usage: jinja render [OPTIONS]

Options:
  -d, --data            PATH to YAML or JSON data file
  -t, --template        PATH to any file that uses Jinja
  -v, --verbose
  -tb, --trim-blocks    Disable trim blocks
  -lb, --lstrip-blocks  Disable lstrip blocks
  -o, --output          PATH for output
  --help                Show this message and exit.
```

## Whitespace Control

`trim_blocks` and `lstrip_blocks` are used by default, to disable them use `-tb` or `-lb` respectively.

## Examples

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

```
➜  jinja2-tools git:(master) jinja render -d examples/data.yaml -t examples/template.sh -lb -tb
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