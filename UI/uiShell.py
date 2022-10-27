import tkinter

from UI.helpers import isValidTweetUrl
from processTweets import twitterSpider 
from settings import API_KEY, API_KEY_SECRET, API_TOKEN_SECRET,API_ACCESS_TOKEN

consumerKey = API_KEY
consumerSecret = API_KEY_SECRET
accessKey = API_ACCESS_TOKEN
accessSecret = API_TOKEN_SECRET


class searchScreen(tkinter.Tk):
    # will have a search box in which you can place a link to a tweet or use a hashtag
    # color pallete: foreground: #4A474C, background: #889495
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Notable Nodes")
        self.configure(background="#889495")
        inputFrame = tkinter.Frame(self, width=600, height=300)
        inputFrame.configure(background="#889495")
        self.userEntry = tkinter.StringVar()
        tkinter.Label(inputFrame, text="Search for a hashtag or paste a link to a tweet", background="#889495", font=("Helvetica", 20) ).pack(pady=10)
        self.searchBox = tkinter.Entry(inputFrame, width=50, textvariable=self.userEntry, highlightbackground="#4A474C",  background="#4A474C", fg="white", font=("Helvetica", 20))
        self.searchBox.pack(pady=5)
        tkinter.Button(inputFrame, text="Search", width=10, height=2, command=self.searchForTweet).pack()

        self.inputMessageBox = None # will have info from the state of a users input
        inputFrame.pack()

        exampleFrame = tkinter.Frame(self, width=600, height=300)
        exampleFrame.configure(background="#889495") # set the background to the same as body
        tkinter.Label(exampleFrame, text="Or analyze Examples", background="#889495", font=("Helvetica", 20) ).grid(column=0, row=0,pady=10)
        KANYE_BUTTON = tkinter.Button(exampleFrame, text="Kanye", width=20, height=5).grid(column=0, row=1, padx=10)
        HOTD_BUTTON = tkinter.Button(exampleFrame, text="House of The Dragon", width=20, height=5).grid(column=1, row=1, padx=10)
        WORLD_CUP_BUTTON = tkinter.Button(exampleFrame, text="Fifa World Cup", width=20, height=5).grid(column=2, row=1, padx=10)
        exampleFrame.pack()

    
    def searchForTweet(self):
        searchTerm = self.userEntry.get()
        # check if url or hashtag


        # first check if tweet url. If not tweet url, check if hashtag with only one word
        if isValidTweetUrl(input) == True:
            self.inputMessageBox.destroy() #destroy the message box if any
            print("tweet:", input)
            self.searchBox.configure(highlightbackground="green", highlightthickness=3)

        elif len(input.split()) == 1 :
            if self.inputMessageBox != None: # destroy the message box if any.
                self.inputMessageBox.destroy() # will remove all message boxes
            print("hashtag:", input) #will show green border to signal that all is well
            self.searchBox.configure(highlightbackground="green", highlightthickness=3)
            spider = twitterSpider(consumerKey, consumerSecret, accessKey, accessSecret, searchTerm, "2022-10-17", 10)
            spider.fetchTweets() 
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


    