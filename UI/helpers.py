import re
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