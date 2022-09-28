import pandas

if __name__ == '__main__':
    mod_list = pandas.read_excel('Mods and Synergy.xlsx', sheet_name=0, header=0)
    mod_list.rename(columns={
        'ID': 'id', 'Name': 'name', 'Slot': 'slot', 'Affinity': 'affinity', 'Cost': 'cost',
        'Stack?': 'stack', 'PvP?': 'pvp', 'Effects': 'effects'
    }, inplace=True)
    mod_list.to_parquet('mod_list.parquet.gzip', engine='pyarrow', compression='gzip')

    # Attributes
    mod_attribute_list_wells = pandas.read_excel('Mods and Synergy.xlsx', sheet_name=1, header=0)
    mod_attribute_list_wells['stack_constraint_mod_id'] = mod_attribute_list_wells['stack_constraint_mod_id'].astype(str)
    mod_attribute_list_wells.to_parquet('mod_attribute_list_wells.parquet.gzip', engine='pyarrow', compression='gzip')

    mod_attribute_list_cwl = pandas.read_excel('Mods and Synergy.xlsx', sheet_name=2, header=0)
    mod_attribute_list_cwl['stack_constraint_mod_id'] = mod_attribute_list_cwl['stack_constraint_mod_id'].astype(str)
    mod_attribute_list_cwl.to_parquet('mod_attribute_list_cwl.parquet.gzip', engine='pyarrow', compression='gzip')

    mod_attribute_list_warmind = pandas.read_excel('Mods and Synergy.xlsx', sheet_name=3, header=0)
    mod_attribute_list_warmind['stack_constraint_mod_id'] = mod_attribute_list_warmind['stack_constraint_mod_id'].astype(str)
    mod_attribute_list_warmind.to_parquet('mod_attribute_list_warmind.parquet.gzip', engine='pyarrow', compression='gzip')

    mod_attribute_list_weapon = pandas.read_excel('Mods and Synergy.xlsx', sheet_name=4, header=0)
    mod_attribute_list_weapon['stack_constraint_mod_id'] = mod_attribute_list_weapon['stack_constraint_mod_id'].astype(str)
    mod_attribute_list_weapon.to_parquet('mod_attribute_list_weapon.parquet.gzip', engine='pyarrow', compression='gzip')
