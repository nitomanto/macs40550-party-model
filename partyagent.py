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
            #initial_state,
            #extro,
            neighbor_dance_thres,
            energy,
            #alcohol,
            alcohol_prop,
            alcohol_dance_thres,
            extro_floor,
            extro_ceiling
    ):
        
        super().__init__(model)

        self.extro_const = self.random.uniform(extro_floor, extro_ceiling)
        self.state = State.PARTY_POOPER
        self.energy = energy
        #self.metabolism = 1
        self.neighbor_dance_thres = neighbor_dance_thres
        self.alcohol_dance_thres = alcohol_dance_thres
        self.drinker = bool(self.random.random() <= alcohol_prop)
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
        else:
            self.neighbor_state = False
    # calculate random extroversion feeling; if less than extro_const, activates extroversion component   
    def assess_extro(self):
        if self.random.random() < self.extro_const:
            self.extro_state = True
        else:
            self.extro_state = False
    # calculate/metabolize energy and changes state if dancing queens run out of energy
    def metabolize(self):
        self.energy = self.energy - (1 * (self.drunkness))

    # calculate alcohol levels
    def assess_alcohol(self):
        if self.drunkness >= self.alcohol_dance_thres:
            self.alcohol_state = True
        else:
            self.alcohol_state = False

    def step(self):
        # first rule out kaputs
        # then assess neighbor, extro, and alcohol states
        # party poopers: at least one thing true to start dancing
        # dancing queen: at least one thing true to keep dancing
        # KAPUTS: stay kaput
        # after updates:
        # dancing queens: metabolize energy
        # party poopers: get drunker (if alcohol)

        if self.energy <= 0:
            self.state = State.KAPUT

        if self.drunkness > self.energy:
            self.state = State.KAPUT
        
        if self.state == State.DANCING_QUEEN:

            #metabolize energy
            self.metabolize()
                # check to continue dancing
            self.assess_alcohol()
            self.assess_extro()
            self.assess_neighbor_prop()

            attributes = [self.alcohol_state, self.neighbor_state, self.extro_state]
            trues = [attr for attr in attributes if attr==True]
            if len(trues) < 1:
                # no incentive to dance, become a party pooper
                self.state = State.PARTY_POOPER
            else:
                    # stay dancing, queen
                self.state = State.DANCING_QUEEN

        elif self.state == State.PARTY_POOPER:

            if self.drunkness > self.energy:
                self.state = State.KAPUT

            else:
            
                self.assess_alcohol()
                self.assess_extro()
                self.assess_neighbor_prop()
                
                attributes = [self.alcohol_state, self.neighbor_state, self.extro_state]
                trues = [attr for attr in attributes if attr==True]
                if len(trues) < 2:
                    # stay party pooper and drink more (if alcohol)
                    self.state = State.PARTY_POOPER
                    if self.drinker:
                        self.drunkness += 1
                else:
                        # become dancing queen and start metabolizing in next step
                    self.state = State.DANCING_QUEEN