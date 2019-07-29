import sys
import argparse
import json

parser = argparse.ArgumentParser(description='Re-arranges list of flat json objects into nested json')
parser.add_argument('keys', nargs='*')


class DictifyError(Exception):
    pass


class NestedError(Exception):
    pass


def dictify(obj_list, key):
    """
    Transform list of dicts into dict of dicts, exctracting the value of `key` from each dict in obj_list.
    :param obj_list:
    :param key:
    :return:
    """
    result = {}
    for obj in obj_list:

        if key not in obj:
            raise DictifyError(f'Key "{key}" not found in {obj}')

        val = obj[key]
        del obj[key]
        if val not in result:
            result[val] = []

        result[val].append(obj)

    return result


def make_nested_dicts(data, keys, level=0):
    """
    Recurcively rebuilds input object into nested dicts using values from keys-list
    If `data` is list - transforms it info dict using the appropriate key from `keys`
    If `data` is dict - apply itself to each value

    :param data:
    :param keys:
    :param level:
    :return:
    """

    if not keys:
        return data

    if level >= len(keys):
        return data

    if type(data) == list:
        data = dictify(data, keys[level])

    if not type(data) == list:
        for key, value in data.items():
            data[key] = make_nested_dicts(value, keys, level+1)

    return data


def main():

    args = parser.parse_args()
    nesting_keys = args.keys

    if not sys.stdin.isatty():
        lines = sys.stdin.read()
    else:
        exit()

    try:
        input_data = json.loads(lines)
    except json.JSONDecodeError:
        sys.stderr.write('Could not json-decode input data')
        exit()

    try:
        result = make_nested_dicts(input_data, nesting_keys)
    except (DictifyError, NestedError) as e:
        sys.stderr.write(str(e))
        exit()

    sys.stdout.write(json.dumps(result))


if __name__ == '__main__':
    main()