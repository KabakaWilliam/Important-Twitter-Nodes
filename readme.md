# Notable Nodes

This project is designed to illustrate the spread of information about a particular topic on twitter. Currently the app can be run in interactive and terminal mode

<br>

### [Demo Video](https://youtu.be/HOZIlo2YQ34)

<br>

## Running the entire Project in terminal mode

### Install dependencies

```bash
#Install required dependencies then run app
$ pip3 install -r requirements.txt
```

## Running the entire Project in interactive mode

```bash
#Install required dependencies then run app
$ pip3 install -r requirements.txt
$ python3 app.py
```

### Run in default terminal mode

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

### Specific File instructions

Run `processTweets.py` to collect tweets that contain specified term in the terminal. This module also contains the `twitterSpider` class which can be imported into the ui module

Please create a .env file and fill out the appropriate environment variables

Tweets will be saved into a `EACOPV3.csv` file

As of now, most of the graph experimentation with networkX is happening in `graphing.py`. In interactive mode, we can see the different subgraphs however, it only defaultlu works with the `House of the Dragon ` dataset. An error I encountered is that I needed to reconfigrue the way I draw the graphs before pickling them.

#### NOTE:

The `House of the Dragon ` dataset is currently the largest default dataset with 50,000 tweets.

The graph drawn in GUI / Interactive mode is static when to compared to the one rendered by the terminal mode.

The Project Proposal is `williamProposal15112.pdf`

`data.csv` and `EACOPV3.csv` are sample files that contain collected twitter data.

### TO DO's:

- [ ] Add EC2 script that will be used to analyze the tweets

- [x] Unpickle the graphs when the buttons in the UI are clicked
- [x] Improve the interactive mode with PyInquirer
- [x] Find a way to make the graphs more interactive when using the GUI
- [x] Import twitter spider into the frontend
- [x] Impelment regex to extract twitter data for a tweet from a user inputed URL
- [x] Port networkX code into main UI.
- [x] Implement page rank with networkX
- [x] Find way to display these results on the screen
