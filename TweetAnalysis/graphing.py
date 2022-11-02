import pandas as pd
import networkx as nx
from collections import Counter 
import matplotlib.pyplot as plt
import os
import pickle
from PyInquirer import prompt


def loadDataset(dataSetPath):
    """
    It reads in the data from the csv file and returns a dataframe with the columns we want
    
    :param dataSetPath: The path to the dataset
    :return: A dataframe with the columns location, retweetcount, text, hashtags, username, and tweetID
    """
    data = pd.read_csv(dataSetPath, lineterminator='\n')
    tweet = data[['location', 'retweetcount', 'text', 'hashtags', 'username', "tweetID"]]
    return tweet


def getMentionedUsers(s):
    """
    It takes a string as input and returns a list of all the users mentioned in the string
    
    :param s: the string to be parsed
    :return: A list of all the users mentioned in the tweet.
    """
    foundAt= False
    mentioned = []
    store = ""
    for i in range(len(s)):
        if s[i] == "@": #a user is mentioned whenever we see @
            foundAt = True
            start = i
            while start != len(s) and  s[start]!= " " and s[start] != "." :
                store += s[start]
                start += 1
            store = store[1:]
            mentioned.append(store)
            store = ""
    return mentioned


def createAdjecencyDictionary(tweetDataframe):
    """
    This function takes in a dataframe of tweets and returns a dictionary of the form {tweetAuthor1:
    [@user1, @user2, @user3, @user4, @user5, @user6]}
    
    The function iterates through the dataframe and checks if the tweet contains a mention. If it does,
    it stores the tweet author and the mentioned users in a dictionary
    
    :param tweetDataframe: the dataframe that contains the tweets
    :return: A dictionary of the form {tweetAuthor1: [@user1, @user2, @user3, @user4, @user5, @user6]}
    """
    # will build adjecency dictionary in the form:
    # {tweetAuthor1: [@user1, @user2, @user3, @user4, @user5, @user6]}
    # create graph of tweet author here.
    adjecencyDictionary=dict()
    for ind in tweetDataframe.index:
        if '@' in tweetDataframe['text'][ind]:
            store = ""
            
            for e in tweetDataframe['text'][ind]:

                if e=='@':
                    store += e

            adjecencyDictionary[tweetDataframe["username"][ind]] = getMentionedUsers(tweetDataframe['text'][ind])
    return adjecencyDictionary

def convertDictionaryToGraph(adjecencyDictionary):
    """
    This function takes in a dictionary of tweet authors and their mentions and returns a directed graph
    of tweet authors and their mentions.
    
    :param adjecencyDictionary: a dictionary of the form {author: [mentions]}
    :return: A directed graph of the tweet author to their mentions.
    """
    # create graph of tweet author to their mentions. 
    # .to_directed converts our graph to a directed graph
    tweetGraph = nx.Graph(adjecencyDictionary).to_directed()
    return tweetGraph

def applyPageRankToGraph(tweetGraph):
    """
    It takes a graph and returns a dictionary of the nodes in the graph and their pageRank scores
    
    :param tweetGraph: the graph we're applying pageRank to
    :return: A dictionary of nodes and their pageRank values
    """
    # apply pageRank to graph. gives us most linked to nodes
    pageRankData = nx.pagerank(tweetGraph, alpha=0.85, weight='weight')
    return pageRankData

def getPageRankSummary(pageRankData, importantNodeCount=10):
    """
    The function takes in a dictionary of nodes and their page rank values, and returns a dictionary of
    the most important nodes and their page rank values
    
    :param pageRankData: This is the data that we want to summarize
    :param importantNodeCount: The number of nodes you want to return in the summary, defaults to 10
    (optional)
    :return: The most influential node and the top nodes with the highest values.
    """
    # store all important top level data in a dictionary
    summaryDict = dict()
    # NOTE: need to account for when there graph has no maximum nodes
    # or rather, no nodes are linked
    mostInfluentialNode = max(pageRankData, key=pageRankData.get)
    summaryDict["mostInfluentialNode"] = {str(mostInfluentialNode): pageRankData[mostInfluentialNode]} #store node with its value

    #Counter will allow us to return max nodes with the highest values
    summaryDict["topNodes"] = dict(Counter(pageRankData).most_common(importantNodeCount))
    print("================================================")
    print("summary :", summaryDict) #will print raw in order to ease visability
    print("================================================")
    return summaryDict

def runMainGraphProcessing(tweet):
    """
    It takes a tweet, creates an adjacency dictionary, converts that dictionary to a graph, applies the
    PageRank algorithm to the graph, and returns the graph and a summary of the PageRank data.
    
    :param tweet: The tweet to be processed
    :return: A list of two items. The first item is the graph object, the second item is a list of
    tuples.
    """
    tweetAdjDictionary = createAdjecencyDictionary(tweet)
    tweetGraph = convertDictionaryToGraph(tweetAdjDictionary)
    pageRankData = applyPageRankToGraph(tweetGraph)
    prSummary = getPageRankSummary(pageRankData)
    return [tweetGraph, prSummary]

def saveSubGraphLocally(figure, topUsers, count, searchTerm):

    searchTerm = searchTerm.split("/")[1]
    PATH = f"PickleData/{searchTerm}"
    # get name for the search term. It has to be separeted from the path
    # Check if it the directory does not exist.
    # if it does not, make the directory
    if not os.path.exists(PATH):
        os.makedirs(PATH)  
    print("figure in File :", figure)
    # save the graph within the directory PickleData with format:
    # PickleData/searchTerm/topUserNodeGraph.fig.pickle
    pickle.dump(figure, open(f'PickleData/{searchTerm}/{topUsers[count]}.fig.pickle', 'wb'))

def drawSubGraphs(tweetGraph, prSummary, searchTerm, graphVisible=True, download=True):
    """
    This function takes a graph and returns a list of subgraphs
    
    :param tweetGraph: the graph we want to draw
    :param graphVisible: if True, will draw the subgraphs. If False, will not draw the subgraphs,
    defaults to True (optional)
    :return: A list of subgraphs
    :param prSummary:  a summary of the page Rank data
    :param searchTerm:  the search term we used
    """
    # function will allow us to draw all subgraphs.
    # need to add a way to draw title of graph/community
    # we will also need to tank the graphs with the highest connectivity
    # can be plugged into the page rank calcultation.
    # have a fucntion to draw all subgraphs or a few graphs
    importantTweetSubgraphs = []
    # return a list of top 10 user nodes
    topUsers = prSummary["topNodes"].keys()
    topUsers = list(topUsers)

    # connected_components returns a list of all connected nodes and edges
    # For this graph we know that each important node(ranked by page rank) has
    # to be connected to at least one node by an edge. We can then loop through
    # all connected_components, check if they have any important nodes and then 
    # create a subgraph which we append to importantTweetSubgraphs and then draw
    # to the screen
    for c in nx.connected_components(tweetGraph):
        g = tweetGraph.subgraph(c)
        # importantTweetSubgraphs.append(g)
        
        # look for subgraph that contain most important users in the graph
        for user in topUsers:
            if user in g:
                importantTweetSubgraphs.append(g) 

    # way to draw the subgraphs for each improtant page rank element

    # ******NOTE******:
    # can be improved later by storing the graphs to a file which we can
    # read to store and visualize
    count = 0 #we will use this counter to get the name for the current user in topUsers
    for g in importantTweetSubgraphs:

           
        nx.draw_spring(g, node_shape="s", with_labels=True, node_size=100, linewidths=0.25,
        bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'))
        if download == True:
            saveSubGraphLocally(g, topUsers, count, searchTerm)
        if graphVisible == True: 
            plt.show()
        count += 1
    return importantTweetSubgraphs

        


def drawGraph(tweetGraph, prSummary, searchTerm, download=True, graphVisible=True):
    """
    If the graph has less than 400 nodes, draw it with the spring layout. Otherwise, draw the subgraphs
    
    :param tweetGraph: the graph we're drawing
    :param prSummary: a summary of the page Rank data
    :Optionalparam download: graph will have its pickle downloaded
    :Optionalparam graphVisible: graph will be displayed
    """
    # return a list of top 10 user nodes
    topUsers = prSummary["topNodes"].keys()
    topUsers = list(topUsers)


    if tweetGraph.number_of_nodes() <= 400:
        nx.draw_spring(tweetGraph, with_labels = True, node_size=100, linewidths=0.25, font_size=15, node_shape="s"
        ,bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'))
        if download == True: #done so we can draw graphs without pickling them
            saveSubGraphLocally(tweetGraph, topUsers, 0, searchTerm)
        if graphVisible == True:
            plt.show()
    else:
        tweetGraph = nx.to_undirected(tweetGraph)
        if download == False: #allows us to view graphs from cache
            mySubGraphs = drawSubGraphs(tweetGraph, prSummary, searchTerm, graphVisible=True, download=False) #can be graphVisible=False to prevent graphs from drawing
        else:
            mySubGraphs = drawSubGraphs(tweetGraph, prSummary, searchTerm, graphVisible=True, download=True) #can be graphVisible=False to prevent graphs from drawing



# main function to be exported to the UI to do the processing
def processTweetsFromPath(PATH):
    """
    It takes a path to a file, loads the file, runs the main graph processing function, and returns
    the graph and a summary of the graph
    
    :param PATH: the path to the dataset
    :return: The return value is a tuple of two elements. The first element is the graph object, the
    second element is a summary of the graph.
    """
    print("selected Path:", PATH)
    tweet = loadDataset(PATH)
    tweetGraph, prSummary = runMainGraphProcessing(tweet)
    return tweetGraph, prSummary



# tweetGraph, prSummary = runMainGraphProcessing(tweet)
# print(tweetGraph["HOTDsource"])



# do any of the most linked to nodes make any tweets?
# if so lets analyse the graph that results from their tweets on this topic




# edge centrality. What communities exist
# go through the graph and delete the nodes that have the highest edge centrality
# i.e the nodes gthat link two different communties together
# NUM_ITERATIONS = 10
# for i in range(NUM_ITERATIONS):
#     edgeBetweeness = nx.edge_betweenness_centrality(tweetGraph).items()
#     edgeToDelete = sorted(edgeBetweeness, key=lambda pair: -pair[1])[0][0]
#     print("importantCommunity", edgeToDelete)

#     tweetGraph.remove_edge(*edgeToDelete)
#     if i == 9:
#         nx.draw(tweetGraph, node_color="r" )
#         plt.title('Step %s\nEdge %s Deleted'%(i, edgeToDelete))
#         plt.show()

# drawGraph(tweetGraph)





def getTopNodes(tweetDataframe):
    """
    We create a graph of the tweet authors and their mentions, then apply the PageRank algorithm to the
    graph to find the most influential tweet authors
    
    :param tweetDataframe: the dataframe of tweets that you want to analyze
    :return: A dictionary of the top 10 nodes with the highest pageRank values.
    """
    # turn tweet dataframe into dictionary
    tweetAdjDictionary = createAdjecencyDictionary(tweetDataframe)

    # create graph of tweet author to their mentions.
    tweetGraph = nx.Graph(tweetAdjDictionary)

    # apply pageRank to graph
    pageRank = nx.pagerank(tweetGraph, alpha=0.85, weight='weight')

    #Counter will allow us to return max nodes with the highest values
    topNodes = dict(Counter(pageRank).most_common(10))

    return topNodes



# rt and mention graph structure
# ref: https://www.oreilly.com/library/view/mining-the-social/9781449394752/ch01s02.html



# edge betweeness
# https://www.youtube.com/watch?v=F4RVBAGJcFYx


def main():
    currentDatasets = os.listdir("dataSets")

    questions = [
        {
            'type':  'list',
            'name': 'user_option',
            'message': 'Choose a data set',
            'choices': currentDatasets
        }
    ]
    
    answers = prompt(questions)
    # dataset cant be empty due to default datasets loaded in
    if answers.get("user_option") in currentDatasets:
        chosenDataset = answers.get("user_option")
        datasetPath = "dataSets" + "/" + chosenDataset + "/" + chosenDataset + ".csv"
        print(chosenDataset + " loaded")
        data = pd.read_csv(datasetPath, lineterminator='\n') #add lineterminator to remove bug with large csv files 

        user = data[['username', 'description', 'following',
        'followers', 'totaltweets', 'accountCreatedAt', 'accountID', "tweetID"]]
        tweet = data[['location', 'retweetcount', 'text',
        'hashtags', 'username', "tweetID"]]

        user.drop_duplicates(subset="username",inplace=True)
        user.username.duplicated().unique()

        tweetGraph, prSummary = runMainGraphProcessing(tweet)
        drawGraph(tweetGraph, prSummary, datasetPath)
        print("Graph drawn to screen")
    else:
        print("error typing in dataset or dataset does not exist")






if __name__ == "__main__":
    main()





# To improve interactivity, use the click library;
# https://click.palletsprojects.com/en/8.1.x/
#  https://dev.to/cotter/how-to-make-an-interactive-todo-list-cli-using-python-with-an-easy-login-mechanism-595h