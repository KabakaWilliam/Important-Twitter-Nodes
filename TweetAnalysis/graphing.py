import pandas as pd
import networkx as nx
from collections import Counter 
import matplotlib.pyplot as plt
from os import listdir

def loadDataset(dataSetPath):
    data = pd.read_csv(dataSetPath, lineterminator='\n')
    tweet = data[['location', 'retweetcount', 'text', 'hashtags', 'username', "tweetID"]]
    return tweet


def getMentionedUsers(s):
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
    # create graph of tweet author to their mentions. 
    # .to_directed converts our graph to a directed graph
    tweetGraph = nx.Graph(adjecencyDictionary).to_directed()
    return tweetGraph

def applyPageRankToGraph(tweetGraph):
    # apply pageRank to graph. gives us most linked to nodes
    pageRankData = nx.pagerank(tweetGraph, alpha=0.85, weight='weight')
    return pageRankData

def getPageRankSummary(pageRankData, importantNodeCount=10):
    # store all important top level data in a dictionary
    summaryDict = dict()
    mostInfluentialNode = max(pageRankData, key=pageRankData.get)
    summaryDict["mostInfluentialNode"] = pageRankData[mostInfluentialNode] #store node with its value

    #Counter will allow us to return max nodes with the highest values
    summaryDict["topNodes"] = dict(Counter(pageRankData).most_common(importantNodeCount))
    print("================================================")
    print("summary :", summaryDict) #will print raw in order to ease visability
    print("================================================")
    return summaryDict

def runMainGraphProcessing(tweet):
    tweetAdjDictionary = createAdjecencyDictionary(tweet)
    tweetGraph = convertDictionaryToGraph(tweetAdjDictionary)
    pageRankData = applyPageRankToGraph(tweetGraph)
    prSummary = getPageRankSummary(pageRankData)
    return [tweetGraph, prSummary]

def drawSubGraphs(tweetGraph, graphVisible=True):
    # function will allow us to draw all subgraphs.
    # need to add a way to draw title of graph/community
    # we will also need to tank the graphs with the highest connectivity
    # can be plugged into the page rank calcultation.
    # have a fucntion to draw all subgraphs or a few graphs
    tweetSubgraphs = []
    for c in nx.connected_components(tweetGraph):
        g = tweetGraph.subgraph(c)
        tweetSubgraphs.append(g)
        if graphVisible == True:
            nx.draw_spring(g, node_color="r", with_labels=True, node_size=100, linewidths=0.25)
            plt.show()
    return tweetSubgraphs

def drawGraph(tweetGraph):
    if tweetGraph.number_of_nodes() <= 400:
        nx.draw_spring(tweetGraph, node_color="r", with_labels = True, node_size=100, linewidths=0.25, font_size=5)
        plt.show()
    else:
        tweetGraph = nx.to_undirected(tweetGraph)
        mySubGraphs = drawSubGraphs(tweetGraph, graphVisible=False)
        print(len(mySubGraphs))
        print(mySubGraphs)


# main function to be exported to the UI to do the processing
def processTweetsFromPath(PATH):
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


if __name__ == "__main__":
    print("Choose a dataset you want to use")
    currentDatasets = listdir("dataSets")

    
    print(currentDatasets)

    datasetInput = input("Enter a dataset: ")
    datasetInput = str(datasetInput)
    if datasetInput in currentDatasets:
        # fotmat the input in the right path format
        datasetInput = "dataSets" + "/" + datasetInput + "/" + datasetInput + ".csv"
        data = pd.read_csv(datasetInput, lineterminator='\n') #add lineterminator to remove bug with large csv files 

        user = data[['username', 'description', 'following',
        'followers', 'totaltweets', 'accountCreatedAt', 'accountID', "tweetID"]]
        tweet = data[['location', 'retweetcount', 'text',
        'hashtags', 'username', "tweetID"]]

        user.drop_duplicates(subset="username",inplace=True)
        user.username.duplicated().unique()

        tweetGraph, prSummary = runMainGraphProcessing(tweet)
        drawGraph(tweetGraph)
        print("Graph drawn to screen")
    else:
        print("error typing in dataset or dataset does not exist")



