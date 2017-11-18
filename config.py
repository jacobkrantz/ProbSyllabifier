#!/usr/bin/env python
import json
import logging as log

with open('config.json') as json_data_file:
    settings = json.load(json_data_file)
    GAConfig = settings["GeneticAlgorithm"]



# set global logging utility

if(settings["logLevel"] == "info"):
    log_level = log.INFO
elif(settings["logLevel"] == "warning"):
    log_level = log.WARNING
else:
    log_level = log.DEBUG

log.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    datefmt='%X',
    level=log_level
)
