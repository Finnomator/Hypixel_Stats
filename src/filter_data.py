import json


data_keys = []


def nested_set(dic: dict, keys: list, value):

    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

    return dic


def safeget(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct


def better_filter(data: dict, filter: dict, keys: list = []):

    global data_keys

    output = {}

    for key in filter:

        if isinstance(filter[key], dict):
            keyss = keys.copy()
            keyss.append(key)
            output[key] = better_filter(data, filter[key], keyss)

        else:
            temp = keys.copy()
            temp.append(key)
            data_keys.append(temp)
            output[key] = safeget(data, *keys)

    return output


def filterit(data, filter_data):

    output = {}

    for keys in data_keys:
        keyss = keys.copy()
        keyss.pop(len(keyss)-2)

        keysss = keys.copy()
        keysss.pop(len(keysss)-1)
        keysss.append(keyss[len(keyss)-1])

        value = safeget(data, *keyss)

        output = nested_set(filter_data, keysss, value)

    return output


def dict_depth(my_dict):
    if isinstance(my_dict, dict):

        return 1 + (max(map(dict_depth, my_dict.values()))
                    if my_dict else 0)

    return 0


def remove_upper(data: dict):

    if len(data) == 1 and dict_depth(data) > 2:
        data = data[list(data.keys())[0]]
        data = remove_upper(data)

    return data


def con_to_dct(filter):

    res = {}

    for key in filter:
        if isinstance(filter[key], dict):
            res[key] = con_to_dct(filter[key])

        elif isinstance(filter[key], list):
            res.update({key: {}})
            for i, a in enumerate(filter[key]):
                res[key].update({filter[key][i]: None})

    return res


def main(data: dict, data_filter: dict, remove_unnecessary_keys=True):

    if list(data.keys()) == ["success", "player"]:
        data = data["player"]

    filter_obj = con_to_dct(data_filter)
    better_filter(data, filter_obj)
    filterit(data, filter_obj)

    if remove_unnecessary_keys:
        filter_obj = remove_upper(filter_obj)

    return filter_obj

    # Yes this code is ( ﾉ ﾟｰﾟ)ﾉ
