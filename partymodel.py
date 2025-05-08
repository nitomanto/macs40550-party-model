# Model File

import numpy as np
import mesa
from mesa import Model
import networkx as nx
from {agents} import {agentclass}

class PartyModel(Model):

    # Init function
    def __init__(self, 
                 #n_agents=30, I'll implement this after doing an initial test
                 # with pre-drawn networks
                 initial_state=0,
                 neighbor_dance_thres=0.5,
                 energy=10,
                 alcohol=False,
                 extro=(0,1),
                 network=None,
                 seed=42):
        #super init random seed
        super.__init__(seed=seed)
        # make network object
        nx_obj = nx.
        self.grid = mesa.space.NetworkGrid(network)