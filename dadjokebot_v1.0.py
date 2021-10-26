from praw import Reddit
import config
import requests

def login():
    print("Logging in...")
    r = Reddit (username = config.username,
             password = config.password,
             client_id = config.client_id,
             client_secret = config.client_secret,
             user_agent = "BigOakBot's Dad Joke Bot v0.1")
    print("Logged in!")
    
    return r


def build_reply(joke):
    body = "Here\'s a knee slapper for ya:\n\n" + "> {0}\n\n".format(joke) + "This joke came from [icanhazdadjoke.com](https://icanhazdadjoke.com)"
    return body


def get_joke():
    return str(requests.get("https://icanhazdadjoke.com/", headers={"Accept":"application/json"}).json()["joke"])


def run(r, comments_replied_to):

    for comment in r.subreddit('learnpython').comments(limit=100):
        if ("!dadjoke" in comment.body) and (comment.id not in comments_replied_to) and (comment.author != r.user.me()):
            print("String with \"!dadjoke\" found in " + comment.id)
            
            joke = get_joke()
            reply = build_reply(joke) 
            comment.reply(reply)
            
            comments_replied_to.append(comment.id) 
            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id +"\n")
            
    
    
def get_saved_comments():
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
    
    return comments_replied_to
        

def main():

    bot = login()
    comments_replied_to = get_saved_comments() #list of comments replied to

    while True:
        run(bot, comments_replied_to)


if __name__ == '__main__':
    main()