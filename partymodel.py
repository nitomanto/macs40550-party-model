# Model File
import random
import numpy as np
import mesa
import math
from mesa import Model
import networkx as nx
from partyagent import PartyAgent, State

def number_state(model, state):
    return sum(1 for a in model.grid.get_all_cell_contents() if a.state is state)

def number_dancing(model):
    return number_state(model, State.DANCING_QUEEN)

def number_static(model):
    return number_state(model, State.PARTY_POOPER)

def number_kaput(model):
    return number_state(model, State.KAPUT)


class PartyModel(Model):

    # Init function
    def __init__(self, 
                 #n_agents=30, I'll implement this after doing an initial test
                 # with pre-drawn networks
                 neighbor_dance_thres=0.5,
                 alcohol_dance_thres=2,
                 energy=10,
                 alcohol_prop=0.5,
                 extro_floor=0,
                 extro_ceiling=1,
                 network_type="florentine",
                 k=2,
                 p=0.01,
                 seed=None):
        #super init random seed
        super().__init__(seed=seed)
        random.seed(seed)
        
        self.neighbor_dance_thres = neighbor_dance_thres
        self.alcohol_dance_thres = alcohol_dance_thres
        self.energy = energy
        self.alcohol_prop = alcohol_prop
        self.extro_floor, self.extro_ceiling = extro_floor, extro_ceiling
        self.network_type = network_type
        self.cum_dq = 0
        self.num_dancing_steps = 0
        # make network object
        if self.network_type=="lesmis":
            self.G = nx.les_miserables_graph()
        elif self.network_type=="southernwomen":
            self.G = nx.davis_southern_women_graph()
        elif self.network_type=="karateclub":
            self.G = nx.karate_club_graph()
        elif self.network_type=="wattsstrogatz":
            self.G = nx.watts_strogatz_graph(25, k, p)
        else:
            self.G = nx.florentine_families_graph()

        self.position = nx.spring_layout(self.G)

        self.grid = mesa.space.NetworkGrid(self.G)

        self.datacollector = mesa.DataCollector(
            {
                "Dancing Queens": number_dancing,
                "Party Poopers": number_static,
                "Kaput": number_kaput,
                "Dancing Queens Ratio": self.dance_ratio,
                "Total Cumulative DQ Integral": self.count_cum_dq,
                "Total Dancing Steps": self.count_dancing_steps
            }
        )

        for node in self.G.nodes():
            a = PartyAgent(
                self,
                self.neighbor_dance_thres,
                self.energy,
                self.alcohol_prop,
                self.alcohol_dance_thres,
                self.extro_floor,
                self.extro_ceiling,
            )

            self.grid.place_agent(a, node)


        self.running = True
        self.datacollector.collect(self)

        if (number_dancing(self)==0) and (number_kaput(self) > (len(self.agents)/3)):
            self.running = False
    

    # Helper function for DataCollector
    def dance_ratio(self):
        try:
            return (number_state(self, State.DANCING_QUEEN) / 
            len(self.agents))
        except ZeroDivisionError:
            return math.inf
        
    def count_cum_dq(self):
        self.cum_dq += number_dancing(self)
        return self.cum_dq
        
    def count_dancing_steps(self):
        if number_dancing(self) > 0:
            self.num_dancing_steps += 1
        return self.num_dancing_steps
        
    def step(self):
        self.agents.shuffle_do("step") 
        self.datacollector.collect(self)           
        
        #if number_dancing(self)==0:
        #if number_kaput(self) > 2:
        #        self.running = False