import pandas as pd
import networkx as nx
from collections import Counter 
import matplotlib.pyplot as plt

# ref: https://stackoverflow.com/questions/33998740/error-in-reading-a-csv-file-in-pandascparsererror-error-tokenizing-data-c-err#:~:text=test_error.csv%27%2C-,lineterminator%3D%27%5Cn,-%27)
data = pd.read_csv("Kanye_300.csv", lineterminator='\n') #add lineterminator to remove bug with large csv files 


user = data[['username', 'description', 'following',
 'followers', 'totaltweets', 'accountCreatedAt', 'accountID', "tweetID"]]
tweet = data[['location', 'retweetcount', 'text',
 'hashtags', 'username', "tweetID"]]

user.drop_duplicates(subset="username",inplace=True)
user.username.duplicated().unique()

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

            adjecencyDictionary[tweetDataframe["username"][ind]] = getMentionedUsers(tweet['text'][ind])
    return adjecencyDictionary

# turn tweet dataframe into dictionary
tweetAdjDictionary = createAdjecencyDictionary(tweet)

# create graph of tweet author to their mentions.
tweetGraph = nx.Graph(tweetAdjDictionary)


# apply pageRank to graph. gives us most linked to nodes
pageRank = nx.pagerank(tweetGraph, alpha=0.85, weight='weight')

print("================================================")
mostInfluentialNode = max(pageRank, key=pageRank.get)
print("max rank node: ", mostInfluentialNode)
print("================================================")

print("================================================")
print(pageRank[mostInfluentialNode])
print("================================================")

#Counter will allow us to return max nodes with the highest values
topNodes = dict(Counter(pageRank).most_common(10))

print("================================================")
print(topNodes)
print("================================================")

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
testD = tweetGraph.to_directed()
print(testD.is_directed())
nx.draw_spring(testD, node_color="r", with_labels = True, node_size=100, linewidths=0.25, font_size=5)


plt.show()


# print(tweetGraph["Koincidence_J"]) #will be the most linked to node

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