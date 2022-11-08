import sys
import pickle
import networkx as nx
import matplotlib.pyplot as plt

# this script should draw the graph in explore mode


def drawGraphFromPickle(PATH, user):
    """
    > This function takes in a path to a pickle file and a user name, loads the pickle file, and draws
    the graph
    
    :param PATH: the path to the pickle file
    :param user: the user you want to explore
    """
    # PATH should be in format PickleData/{searchTerm}/{user}.fig.pickle
    # load the selected pickle and draw it on a different thread to launch
    # in explore mode
    file = open(f'{PATH}', 'rb')
    subgraph = pickle.load(file)
    plt.title(user + " subgraph")
    nx.draw_spring(subgraph, node_shape="s", with_labels=True, node_size=100, linewidths=0.25,
                bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'))
    plt.show()





if __name__ == '__main__':
    print("graphing in explore mode")
    args = sys.argv[1:]
    print(args)
    PATH = args[0]
    user = args[1]
    drawGraphFromPickle(PATH, user)

