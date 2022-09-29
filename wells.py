import copy
from typing import List

import pandas
import pyarrow.parquet as pq
from utility import build_grouped_list_of_equipped_mods


class Wells:
    def __init__(self, equipped_mods: List[int] = None, *args, **kwargs):
        self._equipped_mods = equipped_mods
        self._mod_attribute_list = pq.read_table('mappings/mod_attribute_list_wells.parquet.gzip').to_pandas()
        self._all_copy_mods = self._mod_attribute_list.loc[self._mod_attribute_list['counts_as_copy'] == 1]

    def calculate_count_as_copy_stacks(self, item: dict) -> dict:
        if len(self._all_copy_mods.loc[self._all_copy_mods['mod_id'] == item['mod_id']]) == 0:
            x = sum((self._all_copy_mods['mod_id'] == i).any() for i in list(set(self._equipped_mods)))  # len of UNIQUE copy mods
            item['stack'] = int(item['stack'] + x)
            item['applied_count_as_copy'] = 1

        return item

    def calculate_stack_value(self, stack_count: int, list_of_attributes: pandas.DataFrame):
        curr_value = 0
        actual_stack_count = min(stack_count, len(list_of_attributes))
        for idx in range(actual_stack_count):
            stack_value = list_of_attributes.iloc[idx]
            key = 'stack_value' if idx > 0 else 'value'
            # does the mod require another mod to allow stacking and is the required mod equipped?
            if stack_value['requires_mod'] == 1:
                if int(stack_value['stack_constraint_mod_id']) in self._equipped_mods:
                    curr_value += float(stack_value[key])
            else:
                curr_value += float(stack_value[key])

        return curr_value

    def calculate_stacked_mod(self, list_of_attributes: pandas.DataFrame, curr_obj: dict) -> dict:
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
            curr_obj['curr_value'] = self.calculate_stack_value(curr_obj['stack'], list_of_attributes)
        except Exception as e:
            curr_mod_name = curr_obj['name']
            print(f'Mod: {curr_mod_name} does not stack and is not enabled by anything to stack. Skipping.')

        return curr_obj

    def build_well_stuff(self, obj_list: List[dict]):
        for item in obj_list:
            curr_mod = self._mod_attribute_list.loc[self._mod_attribute_list['mod_id'] == item['mod_id']]
            if len(curr_mod) > 0:
                item['impact'] = curr_mod.iloc[0]['impact']
                item['value_modifier'] = curr_mod.iloc[0]['value_modifier']
                item['curr_value'] = 0
                item = self.calculate_count_as_copy_stacks(item)

                self.calculate_stacked_mod(curr_mod, item)


if __name__ == '__main__':
    list_of_mod_ids = [1, 3, 3, 3, 3, 4, 5, 5]
    myw = Wells(equipped_mods=list_of_mod_ids)
    list_of_grouped_mods = build_grouped_list_of_equipped_mods(list_of_mod_ids)
    myw.build_well_stuff(list_of_grouped_mods)

    print(list_of_grouped_mods)