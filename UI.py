import tkinter
import tkinter.messagebox
from processTweets import twitterSpider 
import customtkinter
from settings import API_KEY, API_KEY_SECRET, API_TOKEN_SECRET,API_ACCESS_TOKEN
import os
from TweetAnalysis.graphing import processTweetsFromPath
import pickle
import matplotlib.pyplot as plt
import networkx as nx



consumerKey = API_KEY
consumerSecret = API_KEY_SECRET
accessKey = API_ACCESS_TOKEN
accessSecret = API_TOKEN_SECRET

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class launchUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x400")
        self.title("Notable Nodes")
        self.label = customtkinter.CTkLabel(master=self, text="NOTABLE NODES", text_color="white", text_font=("Helvetica", 30))
        self.label.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)
        self.subtitle = customtkinter.CTkLabel(master=self, text="Follow the flow of information on Twitter using Page Rank", text_color="gray75", text_font=("Helvetica", 12))
        self.subtitle.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)
        self.button = customtkinter.CTkButton(master=self, text="Launch App", command=self.button_function)
        self.button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    def button_function(self):
        self.destroy()
        print("window closed")

class App(customtkinter.CTk):

    WIDTH = 900
    HEIGHT = 520

    def __init__(self):
        super().__init__()
        self.loading = False #initialize loading state
        self.searchTerm = ""#need to initialize the term being searched for

        # initialize the datasets on load
        self.currentDatasets = os.listdir("dataSets")
        # set the first selected dataset to the first element in the dataset list
        self.selectedDataset = self.currentDatasets[0]
        PATH = f"dataSets/{self.selectedDataset}/{self.selectedDataset}.csv"
        self.tweetGraph, self.pageRankSummary = processTweetsFromPath(PATH)#need to initialize the summary
        self.topUsers = list(self.pageRankSummary["topNodes"].keys())

        self.title("Notable Nodes")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.onClosing)  # call .onClosing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)


        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Available Datasets",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)
 
        self.currentDatasetsVar = tkinter.StringVar(value = self.currentDatasets)
        self.datasetListBox = tkinter.Listbox(self.frame_left,  listvariable = self.currentDatasetsVar,
                                         highlightbackground="#212325",
                                        borderwidth=1, font=("Roboto Medium", -16),
                                        fg="white", bg="#616161")
        self.datasetListBox.bind("<<ListboxSelect>>", lambda  : self.updateSelectedDataset(self.datasetListBox.curselection()))

        self.datasetListBox.grid(row=2, column=0, pady=10, padx=20)


        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Load dataset",
                                                command=self.loadDataset)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)


        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.customAppearanceFunction)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text=f"The most important user for {self.selectedDataset} is:\n" +
                                                        "                                              \n" +
                                                        "                               Jaime\n" ,
                                                   height=300,
                                                   text_font=("Roboto Medium", 15),
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)

        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

        # ============ frame_right ============


        self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_right,
                                                    values=self.topUsers, 
                                                    command=self.drawSelectedGraph)
        self.combobox_1.grid(row=0, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.searchEntry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Search for a hashtag or phrase on twitter")
        self.searchEntry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Seach",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.searchTweetsButtonEvent)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.optionmenu_1.set("Dark")
        self.combobox_1.set("User Graphs")

    def searchTweetsButtonEvent(self):
        print("searching for tweets...")
        self.loading = True # set the loading to True
        self.searchTerm = self.searchEntry.get() 

        # initialize search spider
        # NOTE: Improve by adding a dynamic date widget
        spider = twitterSpider(consumerKey, consumerSecret, accessKey, accessSecret, self.searchTerm, "2022-10-17", 10)
        spiderResponse = spider.fetchTweets() 
        if spiderResponse["success"] == True:
            self.searchEntry.configure(fg_color="green") #set color to green when search goes through
            PATH = spiderResponse["path"] #Filepath to the saved CSV FILE
            self.tweetGraph, self.pageRankSummary = processTweetsFromPath(PATH) #process the files and save the page rank data to state
            
            self.searchEntry.after(4000, lambda : self.searchEntry.configure(fg_color="#343638")) #change color back to normal color
            self.loading = False #loading changed to False
        else:
            # way to visually inform user and developer of an error
            print("error returning spider response")
            self.searchEntry.configure(fg_color="red")
            # red border to signal something has gone wrong
            self.inputMessageBox = tkinter.Message(self, text = "Something went wrong downloading tweets")
            self.inputMessageBox.pack()
            self.loading = False #loading changed to False

    def drawSelectedGraph(self, choice):
        print("Your choice: " + choice)
        # load the specified  pickle containing the subgraph
        file = open(f'PickleData/{self.selectedDataset}/{choice}.fig.pickle', 'rb')
        subgraph = pickle.load(file)
        plt.title(choice + " subgraph")
        nx.draw_spring(subgraph, node_shape="s", with_labels=True, node_size=100, linewidths=0.25,
            bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'))
        plt.show()






    def customAppearanceFunction(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def onClosing(self, event=0):
        self.destroy()
    
    def loadDataset(self):
        # update label
        print("Loading dataset...")
        PATH = f"dataSets/{self.selectedDataset}/{self.selectedDataset}.csv"
        self.tweetGraph, self.pageRankSummary = processTweetsFromPath(PATH)
        mostImportantUser = list(self.pageRankSummary["mostInfluentialNode"].keys())[0] #get start index of value which is the user's name
        self.topUsers = list(self.pageRankSummary["topNodes"].keys())
        # update the main label
        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                text=f"The most important user for {self.selectedDataset} is:\n" +
                                                        "                                              \n" +
                                                        f"                               {mostImportantUser}\n" ,
                                                height=300,
                                                text_font=("Roboto Medium", 15),
                                                corner_radius=6,  # <- custom corner radius
                                                fg_color=("white", "gray38"),  # <- custom tuple-color
                                                justify=tkinter.LEFT)

        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        # update the choicebox
        self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_right,
                                                    values=self.topUsers, 
                                                    command=self.drawSelectedGraph)
        self.combobox_1.grid(row=0, column=2, columnspan=1, pady=10, padx=20, sticky="we")


    def updateSelectedDataset(self, curselection):
        """
        It takes the index of the currently selected item in the listbox, and uses that index to find the
        corresponding item in the list of datasets
        
        :param curselection: a list of the currently selected rows in the table
        """
        # if something was selected
        if len(curselection) > 0:
            self.selectedDataset = self.currentDatasets[curselection[0]]
            print(self.selectedDataset + " selected") 

    def refreshDatasetDirectory(self):
        # run this every 10 seconds to check if theres any change in datasets
        self.currentDatasets = os.listdir("dataSets")
        #NOTE: to improve, rather than delete, you  should just insert the 
        # new dataset. deleting causes glitches
        self.datasetListBox.delete(0, 'end') 
        self.currentDatasetsVar = tkinter.StringVar(value = self.currentDatasets)
        self.datasetListBox = tkinter.Listbox(self.frame_left, listvariable = self.currentDatasetsVar,
                                         highlightbackground="#212325",
                                        borderwidth=1, font=("Roboto Medium", -16),
                                        fg="white", bg="#616161")

        self.datasetListBox.bind("<<ListboxSelect>>", lambda e : self.updateSelectedDataset(self.datasetListBox.curselection()))

        self.datasetListBox.grid(row=2, column=0, pady=10, padx=20)
        
        self.datasetListBox.after(10000, self.refreshDatasetDirectory)

if __name__ == "__main__":
    launchApp = launchUI()
    launchApp.mainloop()
    
    app = App()
    app.refreshDatasetDirectory()
    app.mainloop()
    

