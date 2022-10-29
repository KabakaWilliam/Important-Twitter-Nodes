import tkinter

from UI.helpers import isValidTweetUrl
from processTweets import twitterSpider 
from settings import API_KEY, API_KEY_SECRET, API_TOKEN_SECRET,API_ACCESS_TOKEN

consumerKey = API_KEY
consumerSecret = API_KEY_SECRET
accessKey = API_ACCESS_TOKEN
accessSecret = API_TOKEN_SECRET


class AnalysisWindow(tkinter.Toplevel):
    def __init__(self, parent, YE=False, HOTD=False, FIFA=False, searchTitle=""):
        super().__init__()
        self.geometry('900x400')
        if YE == True:
            self.title("Kanye Twitter Analysis ")
        elif HOTD == True:
            self.title("House of the Dragon Twitter Analysis ")
        elif FIFA == True:
            self.title("World Cup Twitter Analysis ")
        else:
            self.title(searchTitle + "Analysis" )

class searchScreen(tkinter.Tk):
    # will have a search box in which you can place a link to a tweet or use a hashtag
    # color pallete: foreground: #4A474C, background: #889495
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Notable Nodes")
        self.downloadingData = False #flag to help us track when we are downloading/ scraping Tweets
        self.buttonClicked = "" #when a button is clicked, set the title/data here
        self.configure(background="#889495")
        inputFrame = tkinter.Frame(self, width=600, height=300)
        inputFrame.configure(background="#889495")
        self.userEntry = tkinter.StringVar()
        tkinter.Label(inputFrame, text="Search for a hashtag or paste a link to a tweet", background="#889495", font=("Helvetica", 20) ).pack(pady=10)
        self.searchBox = tkinter.Entry(inputFrame, width=50, textvariable=self.userEntry, highlightbackground="#4A474C",  background="#4A474C", fg="white", font=("Helvetica", 20))
        self.searchBox.pack(pady=5)
        tkinter.Button(inputFrame, text="Search", width=10, height=2, command=self.searchForTweet).pack()

        self.openedWindows = set() #store current windows in here.

        self.inputMessageBox = None # will have info from the state of a users input
        inputFrame.pack()

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
    
    def openKanyeAnalysisWindow(self):
        #Will prevent multiple windows from opening
        if "YE" not in self.openedWindows:
            analysisWindow = AnalysisWindow(self, YE=True)
            self.openedWindows.add("YE") #add window to set. 
            analysisWindow.protocol("WM_DELETE_WINDOW", lambda selectedDataset="YE", analysisWindow=analysisWindow : self.removeWindow(selectedDataset, analysisWindow))


    def openHOTDAnalysisWindow(self):
        if "HOTD" not in self.openedWindows:
            analysisWindow = AnalysisWindow(self, HOTD=True)
            self.openedWindows.add("HOTD") #add window to set. 
            analysisWindow.protocol("WM_DELETE_WINDOW", lambda selectedDataset="HOTD", analysisWindow=analysisWindow : self.removeWindow(selectedDataset, analysisWindow))


    def openFIFAAnalysisWindow(self):
        if "FIFA" not in self.openedWindows:
            analysisWindow = AnalysisWindow(self, FIFA=True)
            self.openedWindows.add("FIFA") #add window to set. 
            analysisWindow.protocol("WM_DELETE_WINDOW", lambda selectedDataset="FIFA", analysisWindow=analysisWindow : self.removeWindow(selectedDataset, analysisWindow))
    
    # helper to remove windows already in the set. 
    def removeWindow(self, selectedDataset, analysisWindow):
        self.openedWindows.remove(selectedDataset)
        analysisWindow.destroy()

    
    def openAnalysisWindow(self, windowTitle):
        analysisWindow = AnalysisWindow(self, searchTitle=windowTitle)

    
    def searchForTweet(self):
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
                PATH = spiderResponse["path"]
                self.openAnalysisWindow(searchTerm)
            else:
                # way to visually inform user and developer of an error
                print("error returning spider response")
                self.searchBox.configure(highlightbackground="red", highlightthickness=3)
                # red border to signal something has gone wrong
                self.inputMessageBox = tkinter.Message(self, text = "Something went wrong downloading tweets")
                self.inputMessageBox.pack()

        else:
            print("insert valid tweetURL or hashtag:", input)
            # red border to signal something has gone wrong
            self.searchBox.configure(highlightbackground="red", highlightthickness=3)
            # initialize message box at this point
            self.inputMessageBox = tkinter.Message(self, text = "insert valid tweetURL or hashtag")
            self.inputMessageBox.pack()

if __name__ == "__main__":
    ui = searchScreen()
    ui.mainloop()


    