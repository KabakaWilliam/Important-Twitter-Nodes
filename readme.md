# Notable Nodes

This project is designed to illustrate the spread of information about a particular topic on twitter. Currently the app can be run in interactive and terminal mode

## Running the entire Project in terminal mode

### Install dependencies

```bash
#Install required dependencies then run app
$ pip3 install -r requirements.txt
```

### Run the tweet downloading module

```bash
$ python3 app.py terminal

```

### Run the offline module

```bash
# tweets wont be downloaded
$ python3 app.py terminal offline
```

### NOTE: To bypass the 50 tweet limit

```bash
    input a search term
    $ example%
    #add the % character to bypass the 50 tweet limit

```

## Running the entire Project in interactive mode

```bash
#Install required dependencies then run app
$ pip3 install -r requirements.txt
$ python3 app.py
```

### Specific File instructions

Run `processTweets.py` to collect tweets that contain specified term in the terminal. This module also contains the `twitterSpider` class which can be imported into the ui module

Please create a .env file and fill out the appropriate environment variables

Tweets will be saved into a `EACOPV3.csv` file

As of now, most of the graph experimentation with networkX is happening in `graphing.py`. In interactive mode, we can see the different subgraphs however, it only defaultlu works with the `House of the Dragon ` dataset. An error I encountered is that I needed to reconfigrue the way I draw the graphs before pickling them.

###### Workaround

If you download tweets and search for them in terminal mode, you will be able to render the graphs in both the terminal and gui mode respectively.

The graph drawn is also not as human interactive when to compared to the one rendered by the terminal mode.

The Project Proposal is `williamProposal15112.pdf`

`data.csv` and `EACOPV3.csv` are sample files that contain collected twitter data.

### TO DO's:

- [ ] Add EC2 script that will be used to analyze the tweets
- [ ] Add a date input widget
- [ ] Unpickle the graphs when the buttons in the UI are clicked
- [ ] Improve the interactive mode with PyInquirer
- [ ] Find a way to make the graphs more interactive when using the GUI

- [x] Import twitter spider into the frontend
- [x] Impelment regex to extract twitter data for a tweet from a user inputed URL
- [x] Port networkX code into main UI.
- [x] Implement page rank with networkX
- [x] Find way to display these results on the screen
