import json
import os
import validators


def validate_json(j):
    try:
        ans = json.loads(j)
    except json.decoder.JSONDecodeError:
        return j
    else:
        return ans


def validate_url(url) -> bool:
    return validators.url(url)


def validate_path(path) -> bool:
    return os.path.exists(path) and \
        os.access(os.path.dirname(path), os.R_OK)


def validate_is_file(path) -> bool:
    return validate_path(path) and os.path.isfile(path)


def validate_is_dir(path) -> bool:
    return validate_path(path) and os.path.isdir(path)
