import tkinter
from UI.helpers import isValidTweetUrl
from TweetAnalysis.graphing import processTweetsFromPath
from processTweets import twitterSpider 
from settings import API_KEY, API_KEY_SECRET, API_TOKEN_SECRET,API_ACCESS_TOKEN

consumerKey = API_KEY
consumerSecret = API_KEY_SECRET
accessKey = API_ACCESS_TOKEN
accessSecret = API_TOKEN_SECRET


class AnalysisWindow(tkinter.Toplevel):
    def __init__(self, PATH, parent, YE=False, HOTD=False, FIFA=False, searchTitle=""):

        super().__init__()
        self.geometry('900x500')
        self.PATH = PATH
        if YE == True:
            self.title("Kanye Twitter Analysis ")
        elif HOTD == True:
            self.title("House of the Dragon Twitter Analysis ")
        elif FIFA == True:
            self.title("World Cup Twitter Analysis ")
        else:
            self.title(searchTitle + "Analysis" )

        # initialise top users from pageRankData here
        tweetGraph, prSummary = processTweetsFromPath(self.PATH)
        # return a list of top 10 user nodes
        topUsers = prSummary["topNodes"].keys()
        topUsers = list(topUsers)
        topUsersVar = tkinter.StringVar(value = topUsers)
        
        self.mainFrame = tkinter.Frame(self, width=900,height=500)
        self.TopUserFrame = tkinter.Frame(self.mainFrame, width=900,height=200) 
        tkinter.Label(self.TopUserFrame, text="Top Users").grid(row=0, column=0)
        
        self.userListContainer = tkinter.Frame(self.TopUserFrame, width=900, height=200)
        self.userListWidget = tkinter.Listbox(self.userListContainer, listvariable=topUsersVar, width=900, highlightthickness=0)
        self.userListWidget.pack()
        self.userListContainer.grid(row=1, column = 0)
        self.TopUserFrame.pack()
        self.GraphsFrameContainer = tkinter.Frame(self.mainFrame, width=900,height=200, highlightthickness=3)
        tkinter.Label(self.GraphsFrameContainer, text="Recommended Graphs").grid(row=1, column=0) 

        self.mainGraphContainer = tkinter.Frame(self.GraphsFrameContainer, width=900, height=200, highlightbackground="blue", highlightthickness=3) 
        self.mainGraphContainer.grid(row=2, column=0)

        self.GraphsFrameContainer.pack()


        #use subgraph here. return relevant graphs with nodes in the top 10 page rank list. on click, expand menu
        self.mainFrame.pack()



class searchScreen(tkinter.Tk):
    # will have a search box in which you can place a link to a tweet or use a hashtag
    # color pallete: foreground: #4A474C, background: #889495
    def __init__(self):
        super().__init__()
        self.loading = False #A variabel to intialize the loading state

        self.geometry("800x600")
        self.title("Notable Nodes")
        self.downloadingData = False #flag to help us track when we are downloading/ scraping Tweets
        self.buttonClicked = "" #when a button is clicked, set the title/data here
        self.configure(background="#889495")
        self.inputFrame = tkinter.Frame(self, width=600, height=300)
        self.inputFrame.configure(background="#889495")
        self.userEntry = tkinter.StringVar()
        tkinter.Label(self.inputFrame, text="Search for a hashtag or paste a link to a tweet", background="#889495", font=("Helvetica", 20) ).pack(pady=10)
        self.searchBox = tkinter.Entry(self.inputFrame, width=50, textvariable=self.userEntry, highlightbackground="#4A474C",  background="#4A474C", fg="white", font=("Helvetica", 20))
        self.searchBox.pack(pady=5)
        tkinter.Button(self.inputFrame, text="Search", width=10, height=2, command=self.searchForTweet).pack()

        self.openedWindows = set() #store current windows in here.

        self.inputMessageBox = None # will have info from the state of a users input
        self.inputFrame.pack()

        exampleFrame = tkinter.Frame(self, width=600, height=300)
        exampleFrame.configure(background="#889495") # set the background to the same as body

        # add 3 label forms to center the one in the middle with grid
        tkinter.Label(exampleFrame, text="", background="#889495", font=("Helvetica", 20) ).grid(column=0, row=0,pady=10)
        tkinter.Label(exampleFrame, text="Or analyze Examples", background="#889495", font=("Helvetica", 20) ).grid(column=1, row=0,pady=10)
        tkinter.Label(exampleFrame, text="", background="#889495", font=("Helvetica", 20) ).grid(column=2, row=0,pady=10)
        self.KANYE_BUTTON = tkinter.Button(exampleFrame, text="Kanye", width=20, height=5, command=self.openKanyeAnalysisWindow).grid(column=0, row=1, padx=10)
        self.HOTD_BUTTON = tkinter.Button(exampleFrame, text="House of The Dragon", width=20, height=5, command=self.openHOTDAnalysisWindow).grid(column=1, row=1, padx=10)
        self.WORLD_CUP_BUTTON = tkinter.Button(exampleFrame, text="Fifa World Cup", width=20, height=5,command=self.openFIFAAnalysisWindow).grid(column=2, row=1, padx=10)
        exampleFrame.pack()

        self.fileCache = dict() # cache for openedDataSets
    
    def openKanyeAnalysisWindow(self):
        #Will prevent multiple windows from opening
        if "YE" not in self.openedWindows:
            analysisWindow = AnalysisWindow(PATH="dataSets/Kanye/Kanye.csv",parent = self, YE=True)
            self.openedWindows.add("YE") #add window to set. 
            analysisWindow.protocol("WM_DELETE_WINDOW", lambda selectedDataset="YE", analysisWindow=analysisWindow : self.removeWindow(selectedDataset, analysisWindow))


    def openHOTDAnalysisWindow(self):
        if "HOTD" not in self.openedWindows:
            analysisWindow = AnalysisWindow(PATH="dataSets/HouseOfTheDragon/HouseOfTheDragon2.csv",parent = self, HOTD=True)
            self.openedWindows.add("HOTD") #add window to set. 
            analysisWindow.protocol("WM_DELETE_WINDOW", lambda selectedDataset="HOTD", analysisWindow=analysisWindow : self.removeWindow(selectedDataset, analysisWindow))


    def openFIFAAnalysisWindow(self):
        if "FIFA" not in self.openedWindows:
            analysisWindow = AnalysisWindow(PATH=f'dataSets/worldCup/worldCup.csv',parent = self, FIFA=True)
            self.openedWindows.add("FIFA") #add window to set. 
            analysisWindow.protocol("WM_DELETE_WINDOW", lambda selectedDataset="FIFA", analysisWindow=analysisWindow : self.removeWindow(selectedDataset, analysisWindow))
    
    # helper to remove windows already in the set. 
    def removeWindow(self, selectedDataset, analysisWindow):
        self.openedWindows.remove(selectedDataset)
        analysisWindow.destroy()

    
    def openAnalysisWindow(self, windowTitle, PATH):
        analysisWindow = AnalysisWindow(PATH=PATH, parent= self, searchTitle=windowTitle)

    
    def searchForTweet(self):
        self.loading = True # set the loading to True
        searchTerm = self.userEntry.get()
        # check if url or hashtag



        # first check if tweet url. If not tweet url, check if hashtag with only one word
        if isValidTweetUrl(searchTerm) == True:
            self.inputMessageBox.destroy() #destroy the message box if any
            print("tweet:", searchTerm)
            self.searchBox.configure(highlightbackground="green", highlightthickness=3)

        elif len(searchTerm.split()) == 1 :
            if self.inputMessageBox != None: # destroy the message box if any.
                self.inputMessageBox.destroy() # will remove all message boxes
            print("hashtag:", searchTerm) #will show green border to signal that all is well
            self.searchBox.configure(highlightbackground="green", highlightthickness=3)
            spider = twitterSpider(consumerKey, consumerSecret, accessKey, accessSecret, searchTerm, "2022-10-17", 10)
            spiderResponse = spider.fetchTweets() 
            print("spiderResponse :", spiderResponse)
            if spiderResponse["success"] == True:
                PATH = spiderResponse["path"] #Filepath to the saved CSV FILE
                self.loading = False #loading changed to False
                self.fileCache[searchTerm] = PATH
                self.openAnalysisWindow(searchTerm, PATH)
            else:
                # way to visually inform user and developer of an error
                print("error returning spider response")
                self.searchBox.configure(highlightbackground="red", highlightthickness=3)
                # red border to signal something has gone wrong
                self.inputMessageBox = tkinter.Message(self, text = "Something went wrong downloading tweets")
                self.inputMessageBox.pack()
                self.loading = False #loading changed to False

        else:
            print("insert valid tweetURL or hashtag:", input)
            # red border to signal something has gone wrong
            self.searchBox.configure(highlightbackground="red", highlightthickness=3)
            # initialize message box at this point
            self.inputMessageBox = tkinter.Message(self, text = "insert valid tweetURL or hashtag")
            self.inputMessageBox.pack()
            self.loading = False #loading changed to False

if __name__ == "__main__":
    ui = searchScreen()
    ui.mainloop()



    