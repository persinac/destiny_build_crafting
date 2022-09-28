import copy
from typing import List

import pandas
import pyarrow.parquet as pq
from wells import Wells
from utility import check_if_in_list_of_dict, build_grouped_list_of_equipped_mods


def build_cwl_stuff(mod_list, list_of_mod_ids, obj_list):
    mod_attribute_list = pq.read_table('mappings/mod_attribute_list_cwl.parquet.gzip').to_pandas()
    pass


def build_warmind_stuff(mod_list, list_of_mod_ids, obj_list):
    mod_attribute_list = pq.read_table('mappings/mod_attribute_list_warmind.parquet.gzip').to_pandas()
    pass


def build_weapon_stuff(mod_list, list_of_mod_ids, obj_list):
    mod_attribute_list = pq.read_table('mappings/mod_attribute_list_weapon.parquet.gzip').to_pandas()
    pass


def build_my_stuff(list_of_mod_ids: List[int]):
    myw = Wells(equipped_mods=list_of_mod_ids)
    list_of_grouped_mods = build_grouped_list_of_equipped_mods(list_of_mod_ids)
    myw.build_well_stuff(list_of_grouped_mods)

    return list_of_grouped_mods


if __name__ == '__main__':
    build_my_stuff([1, 3, 3, 3, 3, 4, 5, 5])
