import praw
import config
import time
import requests

def bot_login():
    print ("Logging in...")
    r = praw.Reddit (username = config.username,
             password = config.password,
             client_id = config.client_id,
             client_secret = config.client_secret,
             user_agent = "BigOakBot's Dad Joke Bot v0.1")
    print ("Logged in!")
    
    return r

def run_bot(r, comments_replied_to):
    #print ("Scanning comments...")
            
    for comment in r.subreddit('test').comments(limit=25):
        if "!dadjoke" in comment.body  and comment.id not in comments_replied_to and comment.author != r.user.me():
            print ("String with \"!dadjoke\" found in " + comment.id)
            
            #pulls joke and builds reply as comment_reply
            comment_reply = ("Here's a knee slapper for ya:\n\n")
            joke = requests.get("https://icanhazdadjoke.com/", headers={"Accept":"application/json"}).json()["joke"]
            comment_reply += (">" + str(joke))
            comment_reply += ("\n\n This joke came from [icanhzdadjoke.com](https://icanhazdadjoke.com/)")
            
            comment.reply(comment_reply)#this actually posts the comment built above
            
            #adds comment to replied to list
            comments_replied_to.append(comment.id) 
            with open ("comments_replied_to.txt", "a") as f:
                f.write(comment.id +"\n")
            
    
    #Sleep for 3 seconds
    #print ("Sleeping for 3 seconds.")
    #time.sleep(3)
    
def get_saved_comments():
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
    
    return comments_replied_to
        
    
r = bot_login()
comments_replied_to = get_saved_comments() #list of comments replied to

while True:
    run_bot(r, comments_replied_to)
