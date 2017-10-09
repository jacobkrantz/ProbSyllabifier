#!/usr/bin/env python
import json

with open('config.json') as json_data_file:
    settings = json.load(json_data_file)
    GAConfig = settings["GeneticAlgorithm"]
