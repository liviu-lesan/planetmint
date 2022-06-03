import json

def unwrap_to_string(json_obj):
    return json.dumps(json_obj)

def wrap_to_json(string_obj):
    return json.loads(string_obj)


def wrap_list_to_json(string_list , table):
    holder_list = list()
    asset_holder = {
        'id':'',
        'data':'',
        'tx_id':''
    }
    meta_holder = {
        'id':'',
        'metadata':'',
    }
    if table == 'assets':
        asset_holder["data"]=string_list[0]
        asset_holder["tx_id"]=string_list[1]
        asset_holder["id"]=string_list[2]
        
        
        holder_list.append(asset_holder)
    
    if table == 'metadata':
        meta_holder["id"]=string_list[0]
        meta_holder["metadata"]=string_list[1]
        holder_list.append(meta_holder)
    return holder_list
