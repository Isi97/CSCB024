import praw

class Plugin:
    reddit =  praw.Reddit(client_id='j3ATmmjap3T5ow', \
                     client_secret='L0yRK46oM9bjMfoeNb8bPU5Sbt4', \
                     user_agent='Hype QA', \
                     username='hypeqa', \
                     password='passwordPriority#3')

    rcontent = {"title":[], "body":[]}
    subredditName = ""

    def __init__(self, outputfunction=None, dialogfunction=None):
        self.name = ["reddit"]

        if outputfunction is not None:
            self.out = outputfunction

        if dialogfunction is not None:
            self.showDialog = dialogfunction

    def action(self):
        x = self.showDialog("User input required", "Enter a subreddit: ")

        if x != self.subredditName:
            self.subredditName = x
            self.subreddit = self.reddit.subreddit(x)
            self.hot = self.subreddit.hot(limit=10)

        for submission in self.hot:
            self.rcontent["title"].append(submission.title)
            if submission.selftext != "":
                self.rcontent["body"].append(submission.selftext)
            else :
                self.rcontent["body"].append(submission.url)

        for post in self.rcontent['title']:
            self.out(post+"\n")