import re
import tkinter

from TweetAnalysis.graphing import processTweetsFromPath

def isValidTweetUrl(url):
    """
    It checks if the url is a valid tweet url by checking if it matches 
    the regex format for a tweet url
    
    :param url: the url of the tweet
    :return: A boolean value.
    """
    # example: https://twitter.com/ginnyhogan_/status/1581650885775876096
    # regex format for a tweet is that it contains profile name then status then tweet id
    check = "((https?):\/\/)?(www.)?twitter\.com(\/@?(\w){1,15})\/status\/[0-9]{19}"
    match = re.search(check, url)
    if match != None:
        return True
    return False



def initialiseAnalysisWindow(self):
    tkinter.Label(self, text = "Notable Users", font=("Aerial 15"), background="#889495").grid(row=0, column=0, pady=20)
    tkinter.Label(self, text = "Recommended Graphs", font=("Aerial 15"), background="#889495").grid(row=0, column=1)

    leftFrame = tkinter.Frame(self, width=300, height=400 )
    leftFrame.grid(row=1, column=0)

    # initialise top users from pageRankData here
    tweetGraph, prSummary = processTweetsFromPath(self.PATH, self.searchTerm)
    # return a list of top 10 user nodes
    topUsers = prSummary["topNodes"].keys()
    topUsers = list(topUsers)
    topUsersVar = tkinter.StringVar(value = topUsers)




    # Add a Listbox widget with number as the list items
    listbox =tkinter.Listbox(leftFrame, listvariable=topUsersVar,)
    
    listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    # Configure the Listbox widget to set the width to its content
    listbox.configure(background="#889495", foreground="white", font=('Aerial 24'), width=15, highlightthickness=0, borderwidth=0)

    rightFrame = tkinter.Frame(self, width=500, height=400 )
    rightFrame.configure(background="#000000")

    rightFrame.grid(row=1, column=1)
    for i in range(9):
        #use subgraph here. return relevant graphs with nodes in the top 10 page rank list. on click, expand menu
        tkinter.Button(rightFrame, width=20, height=6, text=f"Graph {i+1}").grid(row=i//3,column=i%3)
    self.configure(background="#889495")
