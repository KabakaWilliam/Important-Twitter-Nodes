# Important Nodes

## Running the entire Project

```bash
#Instal required dependencies then run app
$ pip install -r requirements.txt
$ python3 app.py
```

### Specific File instructions

Run `processTweets.py` to collect tweets that contain specified term in the terminal. This module also contains the `twitterSpider` class which can be imported into the ui module

Please create a .env file and fill out the appropriate environment variables

Tweets will be saved into a `EACOPV3.csv` file

As of now, most of the graph experimentation with networkX is happening in `processing.ipynb`. Will implement this code into
a separate module that will implement page rank.

The Project Proposal is `williamProposal15112.pdf`

`data.csv` and `EACOPV3.csv` are sample files that contain collected twitter data.

### TO DO's:

- [ ] Import twitter spider into the frontend
- [ ] Create a loading indicator for when someone submits a url or hastag on the UI
- [ ] Impelment regex to extract twitter data for a tweet from a user inputed URL
- [ ] Port networkX code into main UI.
- [ ] Introduce filters onto the main tkinter search UI. These should be fed to the twitter spider
- [ ] Implement page rank with networkX
- [ ] Implement Djikstra's algorithm
- [ ] Find way to display these results on the screen
