# batch run test

import mesa
import numpy as np
from partymodel import PartyModel
import json

params = {'neighbor_dance_thres':0.5,
            'alcohol_dance_thres':2,
            'energy':10,
            'alcohol_prop':[0, 0.2, 0.4, 0.6, 0.8],
            'extro_floor':0,
            'extro_ceiling':1,
            'network_type':"southernwomen",
            'seed':[0,2,4,6,8,10]}

results = mesa.batch_run(
PartyModel,
params,
iterations = 1,
max_steps = 100,
#data_collection_period = 1,
number_processes = 1
)

with open('batch_test.json', 'w') as f:
    json.dump(results, f)