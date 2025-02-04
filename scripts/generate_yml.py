#!/usr/bin/python3
# SPDX-License-Identifier: MIT
#
# generate_yml.py
# Generate docs/_data/dsra.yml from initializations/s_Hazard_*.ini
#
# Copyright (C) 2021 Government of Canada
# Author: Damon Ulmi <damon.ulmi@canada.ca>

import os
import configparser
import yaml


# Function to generate name in sentence form
def name_to_sentence(name):
    end = name.split('_')[1]
    title = ''.join(' ' + x if x.isupper() else x for x in end).strip()
    title = title.replace('Val Des Bois', 'Val-des-Bois')
    mag = name[3] + '.' + name[5]
    # return f'{title} - Magnitude {mag}'
    return f'M{mag} {title}'


path = '../FINISHED/'
# Generate list of .md files with proper scenario names
list_of_files = sorted([x for x in os.listdir(path) if x[-3:] == '.md' and x[6] == '_'])

scenarios = []
# Add dict with necessary info to list
for file in list_of_files:
    name = file[:-3]
    long_name = name_to_sentence(name)
    config = configparser.ConfigParser()
    config.read_file(open(f'../initializations/s_Hazard_{name}.ini'))
    description = config.get('general', 'description')
    scenario = {
        'name': name,
        'description': {'en': description, 'fr': ''},
        'title': long_name,
    }
    scenarios.append(scenario)

# Info to start the file, with generated scenarios added
data = {
    'collection': {'en': 'Earthquake Scenarios', 'fr': 'Scénarios de séismes'},
    'id': 'dsra_bc_indicators',
    'title': {'en': 'Seismic Risk', 'fr': 'Risque sismique'},
    'scenarios': scenarios,
}

# Convert to yaml and write file
dump = yaml.dump(data, encoding='utf-8', allow_unicode=True)
resource_file = '../docs/_data/dsra.yml'
with open(resource_file, 'w+b') as f:
    f.write(dump)
