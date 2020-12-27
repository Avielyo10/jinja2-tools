"""
Validators
"""
import json
import os
import validators


def validate_json(j):
    """Try to parse as JSON, if it fails return it as a raw string"""
    try:
        ans = json.loads(j)
    except json.decoder.JSONDecodeError:
        return j
    else:
        return ans


def validate_url(url) -> bool:
    """Try to parse as URL"""
    return validators.url(url)


def validate_path(path) -> bool:
    """Validate that the path exist & have permisions to read from"""
    return os.path.exists(path) and \
        os.access(os.path.dirname(path), os.R_OK)


def validate_is_file(path) -> bool:
    """validate_path(path) and is a file"""
    return validate_path(path) and os.path.isfile(path)


def validate_is_dir(path) -> bool:
    """validate_path(path) and is a directory"""
    return validate_path(path) and os.path.isdir(path)
