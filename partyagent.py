## party agent file

from enum import Enum

from mesa import Agent

class State(Enum):
    PARTY_POOPER = 0
    DANCING_QUEEN = 1
    KAPUT = 2

class PartyAgent(Agent):
    def __init__(
            self,
            model,
            initial_state,
            extro,
            neighbor_dance_thres,
            energy,
            alcohol,
    ):
        
        super().__init__(model)

        self.extro_const = self.random.uniform(extro[0], extro[1])
        self.state = initial_state
        self.energy = energy
        #self.metabolism = 1
        self.neighbor_dance_thres = neighbor_dance_thres
        self.alcohol = alcohol
        self.drunkness = 1
        # the following attributes are used each step to activate dancing
        self.alcohol_state = False
        self.extro_state = False
        self.neighbor_state = False

    # calculate proportion of neighbors dancing, if it's above thres, it activates neighbor component
    def assess_neighbor_prop(self):
        neighbors_nodes = self.model.grid.get_neighborhood(
            self.pos, include_center=False)
        
        dancing_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.DANCING_QUEEN
        ]

        if (len(dancing_neighbors) / len(neighbors_nodes)) \
            >= self.neighbor_dance_thres:
            self.neighbor_state = True
    # calculate random extroversion feeling; if less than extro_const, activates extroversion component   
    def assess_extro(self):
        if self.random.random() < self.extro_const:
            self.extro_state = True
        else:
            self.extro_state = False
    # calculate/metabolize energy and changes state if dancing queens run out of energy
    def assess_energy(self):
        if self.state==State.DANCING_QUEEN:
            self.energy -= 1 * (self.drunkness)
        if self.energy <= 0:
            self.state = State.KAPUT
    # calculate alcohol levels
    def assess_alcohol(self):
        if self.state==State.PARTY_POOPER:
            self.drunkness += 1

        
