import copy
from typing import List
import pyarrow.parquet as pq


def check_if_in_list_of_dict(dict: List[dict], mod_id: int):
    for idx, elem in enumerate(dict):
        if mod_id == elem['mod_id']:
            return idx
    return -1

def build_my_stuff(list_of_mod_ids):
    mod_list = pq.read_table('mappings/mod_list.parquet.gzip').to_pandas()
    mod_attribute_list = pq.read_table('mappings/mod_attribute_list.parquet.gzip').to_pandas()
    equipped_mods = list_of_mod_ids
    obj = {
        'mod_id': 0,
        'impact': '',
        'value_modifier': '',
        'stack': '',
        'curr_value': ''
    }
    list_of_objs = []
    for m_id in equipped_mods:
        if m_id == '' or m_id is None:
            continue
        curr_mod = mod_list.loc[mod_list['id'] == m_id]
        curr_mod_name = curr_mod.iloc[0]['name']
        curr_mod_attribute = mod_attribute_list.loc[mod_attribute_list['mod_id'] == m_id]
        attr_obj = copy.deepcopy(obj)
        attr_obj['mod_id'] = m_id
        attr_obj['impact'] = curr_mod_attribute.iloc[0]['impact']
        attr_obj['value_modifier'] = curr_mod_attribute.iloc[0]['value_modifier']
        attr_obj['curr_value'] = curr_mod_attribute.iloc[0]['value']
        attr_obj['stack'] = 1
        attr_obj['applied_count_as_copy'] = 0

        attr_value = curr_mod_attribute.iloc[0]['value']
        found_idx = check_if_in_list_of_dict(list_of_objs, m_id)
        if found_idx > -1:
            attr_obj = list_of_objs[found_idx]
            attr_obj['stack'] += 1
            curr_value = attr_obj['curr_value']

            try:
                mod_stack = curr_mod_attribute.iloc[attr_obj['stack'] - 1]
                # does the mod require another mod to allow stacking and is the required mod equipped?
                if mod_stack['requires_mod'] == 1:
                    if mod_stack['stack_constraint_mod_id'] in equipped_mods:
                        curr_value += mod_stack['stack_value']
                        attr_obj['curr_value'] = float(curr_value)
                else:
                    curr_value += mod_stack['stack_value']
                    attr_obj['curr_value'] = float(curr_value)
            except Exception as e:
                print(f'Mod: {curr_mod_name} does not stack and is not enabled by anything to stack. Skipping.')

        if found_idx < 0:
            list_of_objs.append(attr_obj)
        else:
            list_of_objs[found_idx] = attr_obj

    # apply the count as copy mods
    all_copy_mods = mod_attribute_list.loc[mod_attribute_list['counts_as_copy'] == 1]

    for obj in list_of_objs:
        checker = all_copy_mods.loc[all_copy_mods['mod_id'] == obj['mod_id']]
        if len(checker) > 0:  # skip if curr item is a copy mod
            continue
        curr_mod_attribute = mod_attribute_list.loc[mod_attribute_list['mod_id'] == obj['mod_id']]
        x = sum((all_copy_mods['mod_id'] == i).any() for i in list(set(equipped_mods)))  # len of UNIQUE copy mods

        obj['stack'] = int(min((obj['stack'] + x), len(curr_mod_attribute)))
        curr_value = 0
        for i in range(obj['stack']):
            mod_stack = curr_mod_attribute.iloc[int(i)]
            curr_value += mod_stack['stack_value']
        obj['curr_value'] = float(curr_value)

    print(list_of_objs)
    return list_of_objs

if __name__ == '__main__':
    build_my_stuff([1,3,3,3,3,"",""])
