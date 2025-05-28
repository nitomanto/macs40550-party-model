# partyapp!!!!

import mesa
import math
import solara
import networkx as nx
from matplotlib.figure import Figure
from partymodel import (
    State,
    PartyModel,
    number_kaput,
    number_dancing
)
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)
from mesa.visualization.utils import update_counter

# Define model parameters
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "neighbor_dance_thres": Slider(
        label="Neighbor Dance Threshold",
        value=0.5,
        min=0,
        max=1,
        step=0.1,
    ),
    "alcohol_dance_thres": Slider(
        label="Alcohol Dance Threshold",
        value=2,
        min=2,
        max=10,
        step=1,
    ),
    "network_type": {
        "type": "Select",
        "value": "florentine",
        "values": ["florentine", "lesmis", 'southernwomen', 'karateclub',
                   'wattsstrogatz',],
        "label": "Network Type",
    },
    "k":{
        "type": "Select",
        "value": 2,
        "values": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        "label": "Watts-Strogatz k value"
    },
    "p": Slider(
            label="Watts-Strogatz p value",
            value=0.01,
            min=0.01,
            max=0.1,
            step=0.01
        )
    ,
    "energy": Slider(
        label="Agent Energy",
        value=10,
        min=1,
        max=20,
        step=1,
    ),
    "alcohol_prop": Slider(
        label="Proportion of Alcohol Drinkers",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1,
    ),
    "extro_floor": Slider(
        label="Extroversion Floor",
        value=0,
        min=0.0,
        max=1.0,
        step=0.1,
    ),
    "extro_ceiling": Slider(
        label="Extroversion Ceiling",
        value=1,
        min=0.0,
        max=1.0,
        step=0.1,
    ),
}

def agent_portrayal(agent):
    node_color_dict = {
        State.PARTY_POOPER: "green",
        State.DANCING_QUEEN: "pink",
        State.KAPUT: "blue",
    }
    return node_color_dict[agent.state]

@solara.component
def NetPlot(model):
    # Set this to update every turn, define it as mpl figure
    update_counter.get()
    fig = Figure()
    ax = fig.subplots()
    # Get dictionary mapping individual nodes to colors based on infection status
    color_dict = {}
    for node in model.G.nodes():
        color_dict[node] = agent_portrayal(model.grid.get_cell_list_contents([node])[0])
    # Get list of colors for each node based on dictionary
    node_colors = [color_dict[node] for node in model.G.nodes()]
    # Draw network graph based on colors defined here and node positions/edge weights defined in the model
    nx.draw(model.G,
            ax=ax,
            pos = model.position,
            node_color=node_colors,
            #width = model.weights
            )
    # Plot the figure
    solara.FigureMatplotlib(fig)

def post_process_lineplot(ax):
    ax.set_ylim(ymin=0)
    ax.set_ylabel("# people")
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")

# Make line plot showing levels of agent statuses over time
StatePlot = make_plot_component(
    {"Party Poopers": "green", "Dancing Queens": "pink", "Kaput": "blue"},
    post_process=post_process_lineplot,
)

def get_dance_ratio(model):
    ratio = model.dance_ratio()
    ratio_text = r"$\infty$" if ratio is math.inf else f"{ratio:.2f}"
    kaput_text = str(number_kaput(model))
    cum_dq_text = str(model.cum_dq)
    dance_period = str(model.num_dancing_steps)

    return solara.Markdown(
        f"Dancing Queens Ratio: {ratio_text}<br>Kaputs: {kaput_text}\
            <br>Cumulative Dancing: {cum_dq_text}\
                <br>Cumulative Dance Period: {dance_period}"
    )

model1 = PartyModel()

# Define page components
page = SolaraViz(
    model1,
    components=[
        NetPlot,
        StatePlot,
        get_dance_ratio,
    ],
    model_params=model_params,
    name="Party Model",
)
# Return page
page 