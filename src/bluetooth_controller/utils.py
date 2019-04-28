def fix_keys(d):
    to_ret = {}
    for key, value in d.items():
        to_ret[key.replace("-", "_")] = value

    return to_ret
