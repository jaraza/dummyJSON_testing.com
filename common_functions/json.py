def remove_ids(origin_dict):
    """
    удаляет ключи из словаря, в которых есть id
    :param origin_dict: исходный словарь
    :return: словарь с удаленными id
    """

    def rmv_ids(node):
        remove_keys = []
        if isinstance(node, dict):
            for key, value in node.items():
                rmv_ids(value)
                if key == 'id':
                    remove_keys.append(key)
            for key in remove_keys:
                del node[key]
        elif isinstance(node, list):
            for item in node:
                rmv_ids(item)

    res = origin_dict.copy()
    rmv_ids(res)
    return res

def remove_tokens(origin_dict):
    """
    удаляет ключи из словаря, в которых есть *Token*
    :param origin_dict: исходный словарь
    :return: словарь с удаленными токенами
    """
    def rmv_tokens(node):
        remove_keys = []
        if isinstance(node, dict):
            for key, value in node.items():
                rmv_tokens(value)
                if "token" in key.lower():
                    remove_keys.append(key)
            for key in remove_keys:
                del node[key]
        elif isinstance(node, list):
            for item in node:
                rmv_tokens(item)

    res = origin_dict.copy()
    rmv_tokens(res)
    return res

def remove_dynamic_data(origin_dict):
    """
    удаляет динамические ключи из словаря
    :param origin_dict: исходный словарь
    :return: словарь с удаленными токенами
    """
    res =  remove_ids(origin_dict)
    res =  remove_tokens(res)
    res.pop("userAgent", None)
    return res

def compare_json_left_in_right(json1, json2, key='', path=''):
    """
    сравнивает, что все значения ключей из json1 есть в json2, лишние ключи из левого json - игнорируются
    :param json1: эталонный словарь
    :param json2: словарь, сравниваемый с эталоном
    :param key: корневое имя ключа
    :param path: путь до ключа, в котором произошло несовпадение значений
    :return: если в правом словаре есть несовпадения значений со значений из левого словаря, возвращается словарь
        формата {"ключ_в_котором_произошло_различие": {"expected": value, "actual": value, "path": полный_путь_до_ключа}}
    """
    diff_dict = {}
    if isinstance(json1, dict) and isinstance(json2, dict):
        for key in json1:
            if key not in json2:
                diff_dict[key] = {"expected": json1[key], "actual": "key undefined", "path": f"{path}{key}"}
                continue
            diff_dict.update(compare_json_left_in_right(json1[key], json2[key], key, f"{path}{key}:"))
    elif json1 != json2:
        diff_dict[key] = {"expected": json1, "actual": json2, "path": path[:-1]}
    return diff_dict