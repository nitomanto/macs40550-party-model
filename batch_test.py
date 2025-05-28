# batch run test

import mesa
import numpy as np
from partymodel import PartyModel
import json

params = {'neighbor_dance_thres':np.linspace(0.1, 1, 10),
            'alcohol_dance_thres': range(2, 5),
            'energy':15,
            'alcohol_prop':[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
            'extro_floor':0,
            'extro_ceiling':1,
            'k': range(2,16),
            'p': np.arange(0.01, 0.11, 0.01),
            'network_type':"wattsstrogatz",
            'seed':[0,2,4,6,8,10]}

if __name__=="__main__":

    results = mesa.batch_run(
    PartyModel,
    params,
    iterations = 1,
    max_steps = 100,
    #data_collection_period = 1,
    number_processes = 20
    )

    with open('batch_test_midway.json', 'w') as f:
        json.dump(results, f)

    print('all done!')