# this is a terrible file please update
import copy
from typing import List

import pandas
import pyarrow.parquet as pq

BASE_OBJ = {
    'mod_id': 0,
    'impact': '',
    'value_modifier': '',
    'stack': 0,
    'curr_value': ''
}


def check_if_in_list_of_dict(dict: List[dict], mod_id: int) -> int:
    for idx, elem in enumerate(dict):
        if mod_id == elem['mod_id']:
            return idx
    return -1


def build_grouped_list_of_equipped_mods(equipped_mods: List[int]) -> List[dict]:
    mod_list = pq.read_table('mappings/mod_list.parquet.gzip').to_pandas()
    list_of_objs = []
    for m_id in equipped_mods:
        if m_id == '' or m_id is None:
            continue
        curr_mod = mod_list.loc[mod_list['id'] == m_id]
        curr_mod_name = curr_mod.iloc[0]['name']
        attr_obj = copy.deepcopy(BASE_OBJ)
        attr_obj['name'] = curr_mod_name
        attr_obj['mod_id'] = m_id
        attr_obj['stack'] = 1
        attr_obj['applied_count_as_copy'] = 0

        found_idx = check_if_in_list_of_dict(list_of_objs, m_id)
        if found_idx > -1:
            attr_obj = list_of_objs[found_idx]
            attr_obj['stack'] += 1
        else:
            list_of_objs.append(attr_obj)

    return list_of_objs