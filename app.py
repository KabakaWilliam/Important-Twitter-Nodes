# Name: William Gitta Lugoloobi
# NetID: wlugoloo
# Assignment: 15-112 FINAL PROJECT
# Project Name: Notable Nodes
# Description: Identify the way information flows on twitter and visualzie it
# Total line Count: 888
# Lines: (app.py ==> 50, UI.py ==> 276, graphing.py ==> 366, processTweets.py ==> 160,
# customGraph.py ==> 37 )

import sys
import os

from UI import launchUI, App

# This is the main function that runs the app. It checks if the user is running the app in interactive
# mode or terminal mode.
if __name__ == "__main__":
    # check if user is running app in interactive or terminal mode
    # the app will run in interactive mode by default, but you can run it
    # in terminal mode by using the terminal flag
    # main flags:
    #       terminal: runs app in terminal mode
    #       offline: runs app in terminal mode witout the need to download tweets

    args = sys.argv[1:] #use index 1 to cut out the initial argument which is the script name
    if "terminal" not in args:
        
        launchApp = launchUI()
        launchApp.mainloop()
        
        app = App()
        app.refreshDatasetDirectory()
        app.mainloop()
    
    # will run the app in terminal mode without the ability to download tweets
    elif "offline" in args:
        print("================================================")
        print(" ")
        print("Running app in offline  terminal mode 💸  📈")
        print(" ")
        print("================================================")
        print(" ")
        os.system("python3 TweetAnalysis/graphing.py") #run this script to apply analysis to the dataset
        print(" ")
        print("SEE YOU AGAIN!🔥")
    # will run when someone wants to download data and graph it
    else:
        print("Running app in terminal mode 👨‍💻 👾 📈")
        os.system("python3 processTweets.py") #run this script to download tweets
        os.system("python3 TweetAnalysis/graphing.py") #run this script to apply analysis to the dataset
        print("SEE YOU AGAIN!🔥")

