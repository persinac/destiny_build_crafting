import pandas

if __name__ == '__main__':
    mod_list = pandas.read_excel('Mods and Synergy.xlsx', sheet_name=0, header=0)
    mod_list.rename(columns={
        'ID': 'id', 'Name': 'name', 'Slot': 'slot', 'Affinity': 'affinity', 'Cost': 'cost',
        'Stack?': 'stack', 'PvP?': 'pvp', 'Effects': 'effects'
    }, inplace=True)
    mod_list.to_parquet('mod_list.parquet.gzip', engine='pyarrow', compression='gzip')

    # Attributes
    mod_attribute_list = pandas.read_excel('Mods and Synergy.xlsx', sheet_name=1, header=0)
    mod_attribute_list.rename(columns={
        'ID': 'id', 'Mod ID': 'mod_id', 'Impact': 'impact', 'Value Modifier': 'value_modifier', 'Value': 'value',
        'stack value': 'stack_value', 'stack constraint mod ID': 'stack_constraint_mod_id', 'requires mod': 'requires_mod'
    }, inplace=True)
    mod_attribute_list.to_parquet('mod_attribute_list.parquet.gzip', engine='pyarrow', compression='gzip')
