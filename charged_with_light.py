import copy
from typing import List

import pandas
import pyarrow.parquet as pq
from utility import build_grouped_list_of_equipped_mods


class ChargedWithLight:
    def __init__(self, equipped_mods: List[int] = None, subclass_match: bool = False, *args, **kwargs):
        self._equipped_mods = equipped_mods
        self._mod_attribute_list = pq.read_table('mappings/mod_attribute_list_cwl.parquet.gzip').to_pandas()
        self._assume_subclass_match = subclass_match

        # filter equipped mods to only CWL mods and use that in build_cwl_stuff()

    def subclass_match_elemental_charge(self, mod_id: int, obj: dict):
        # 18
        if mod_id == 18 and self._assume_subclass_match:
            obj['curr_value'] = 2
            obj['notes'] = "Only gain 2 stacks IF collect well of same sub-class element, else gain 1 stack"

        return obj

    def calculate_stack_value(self, stack_count: int, list_of_attributes: pandas.DataFrame):
        curr_value = 0
        actual_stack_count = min(stack_count, len(list_of_attributes))
        for idx in range(actual_stack_count):
            stack_value = list_of_attributes.iloc[idx]
            key = 'stack_value' if idx > 0 else 'value'
            # does the mod require another mod to allow stacking and is the required mod equipped?
            if stack_value['requires_mod'] == 1:
                multi_id = list(map(int, stack_value['stack_constraint_mod_id'].split(',')))
                if multi_id in self._equipped_mods:
                    curr_value += float(stack_value[key])
            elif stack_value['cwl_subclass_match'] == 1:
                if self._assume_subclass_match:
                    curr_value += float(stack_value[key])
            else:
                curr_value += float(stack_value[key])

        return curr_value

    def calculate_stacked_mod(self, list_of_attributes: pandas.DataFrame, curr_obj: dict, reference_attr: dict) -> dict:
        """Given a mapped mod with counts, calculate the stacked value

        Parameters
        ----------
        list_of_attributes :
        curr_obj :
        equipped_mods :

        Returns
        -------

        """
        try:
            curr_obj['curr_value'] = self.calculate_stack_value(reference_attr['stack'], list_of_attributes)
            self.subclass_match_elemental_charge(reference_attr['mod_id'], curr_obj)
        except Exception as e:
            curr_mod_name = curr_obj['name']
            print(f'Mod: {curr_mod_name} does not stack and is not enabled by anything to stack. Skipping.')

        return curr_obj

    def build_cwl_stuff(self, obj_list: List[dict]):
        for item in obj_list:
            curr_mod = self._mod_attribute_list.loc[self._mod_attribute_list['mod_id'] == item['mod_id']]
            if len(curr_mod) > 0:
                grouped_impact_ids = list(curr_mod["impact_id"].unique())
                impact_list = []
                for impact_id in grouped_impact_ids:
                    temp = {}
                    mod_by_impact = curr_mod.loc[impact_id == curr_mod['impact_id']]
                    temp['impact'] = mod_by_impact.iloc[0]['impact']
                    temp['value_modifier'] = mod_by_impact.iloc[0]['value_modifier']
                    temp['curr_value'] = 0
                    if mod_by_impact.iloc[0]['cwl_subclass_match'] == 1 and self._assume_subclass_match:
                        self.calculate_stacked_mod(mod_by_impact, temp, item)
                        impact_list.append(temp)
                    elif mod_by_impact.iloc[0]['cwl_subclass_match'] == 0:
                        self.calculate_stacked_mod(mod_by_impact, temp, item)
                        impact_list.append(temp)

                item['impact'] = impact_list

        # this won't work until we filter out only applicable CWL mods
        return {'cwl': obj_list}


if __name__ == '__main__':
    assume_subclass_match = True
    list_of_mod_ids = [18, 45]
    myw = ChargedWithLight(equipped_mods=list_of_mod_ids, subclass_match=assume_subclass_match)
    list_of_grouped_mods = build_grouped_list_of_equipped_mods(list_of_mod_ids)
    myw.build_cwl_stuff(list_of_grouped_mods)

    print(list_of_grouped_mods)
