import json

def unwrap_to_string(json_obj):
    return json.dumps(json_obj)

def wrap_to_json(string_obj):
    return json.loads(string_obj)


def wrap_list_to_json(string_list):
    holder = list()
    for x in string_list:
        holder.append(wrap_to_json(x))
    return holder
