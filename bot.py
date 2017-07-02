import praw
from time import sleep
import datetime
import os

# TODO - if user does not have any NSFW comments/posts change string
# TODO - check if user/sub is banned
# TODO - implement functionality of calling info for other users

def get_nsfw_info(reddit, username, time_filter, is_post):
    if is_post:
        for post in reddit.redditor(username).submissions.top(time_filter=time_filter):
            if post.over_18:
                return post.score
    elif not is_post:
        for comment in reddit.redditor(username).comments.top(time_filter=time_filter):
            if comment.over_18:
                return comment.score

def get_nsfw_post_link(reddit, username, time_filter):
    for post in reddit.redditor(username).submissions.top(time_filter=time_filter):
        if post.over_18:
            return post.url

def delete_comment():
    limit = 500
    threshold = 0

    for bot_comment in bot_profile.comments.new(limit=limit):
        if bot_comment.score < threshold:
            bot_comment.delete()

def get_karma(reddit, username):
    return reddit.redditor(username).link_karma

def get_info(reddit, username, time_filter, is_post):
    if is_post:
        for post in reddit.redditor(username).submissions.top(time_filter=time_filter):
            return post.score
    elif not is_post:
        for comment in reddit.redditor(username).comments.top(time_filter=time_filter):
            return comment.score

def get_post_link(reddit, username, time_filter):
    for post in reddit.redditor(username).submissions.top(time_filter=time_filter):
        return post.url

def message(reddit, username, subject, body):
    redditor = reddit.redditor(username).message(subject, body)
    time.sleep(5)

def txt_to_list(filepath):
    return_list = []
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            return_list = f.read()
            return_list = return_list.split("\n")
            return_list = list(filter(None, return_list))
    return return_list

def comment_reply(comment, nsfw):
    reply = ""
    nsfw_filter_string = ""
    blacklist_url = "https://www.reddit.com/r/PythonInfoBotTest/comments/6k79wh/blacklist/"
    footer_string = "^I'm ^a ^bot. ^| ^[Blacklist](" + blacklist_url + ")"
    end_line_string = "\n\n *** \n\n"

    user_karma = get_karma(reddit, comment.author.name)
    user_hot_comment = get_info(reddit, comment.author.name, "year", False)
    user_hot_post = get_info(reddit, comment.author.name, "year", True)
    user_hot_post_link = get_post_link(reddit, comment.author.name, "year")

    user_nsfw_comment = get_nsfw_info(reddit, comment.author.name, "year", False)
    user_nsfw_post = get_nsfw_info(reddit, comment.author.name, "year", True)
    user_nsfw_post_link = get_nsfw_post_link(reddit, comment.author.name, "year")

    if nsfw:
        nsfw_filter_string = "[NSFW]"
        reply = "{name}: *{author}* {nsfw_string}".format(name=bot_name, author=comment.author.name, nsfw_string=nsfw_filter_string)
        reply += "\n\n"
        reply += "User Post Karma: {karma}".format(karma=user_karma)
        reply += "\n\n"
        reply += "{author}'s Hot Post from this Year: {post} upvotes @ {link}".format(author=comment.author.name, post=user_hot_post, link=user_hot_post_link)
        reply += "\n\n"
        reply += "{author}'s Hot Comment from this Year: {comment} upvotes".format(author=comment.author.name, comment=user_hot_comment)
        reply += "\n\n"
        reply += "{author}'s Hot **NSFW** Post from this Year: {post} upvotes @ {link}".format(author=comment.author.name, post=user_nsfw_post, link=user_nsfw_post_link)
        reply += "\n\n"
        reply += "{author}'s Hot **NSFW** Comment from this Year: {comment} upvotes".format(author=comment.author.name, comment=user_nsfw_comment)
        reply += end_line_string
        reply += footer_string
    elif not nsfw: 
        nsfw_filter_string = ""
        reply = "{name}: *{author}* {nsfw_string}".format(name=bot_name, author=comment.author.name, nsfw_string=nsfw_filter_string)
        reply += "\n\n"
        reply += "User Post Karma: {karma}".format(karma=user_karma)
        reply += "\n\n"
        reply += "{author}'s Hot Comment from this Year: {comment}".format(author=comment.author.name, comment=user_hot_comment)
        reply += "\n\n"
        reply += "{author}'s Hot Post from this Year: {post} @ {link}".format(author=comment.author.name, post=user_hot_post, link=user_hot_post_link)
        reply += end_line_string
        reply += footer_string
    return reply

def reply_to_comment(reddit, subreddit, amount):
    for comment in reddit.subreddit(subreddit).comments(limit=amount):
        if call_word in comment.body and comment.author != reddit.user.me():
            exclude_nsfw = exclude_nsfw_string not in comment.body[-5:]
            reply = comment_reply(comment, exclude_nsfw)
            print("replying..")
            comment.reply(reply)

            #with open(comments_replied_filename, "a") as f:
             #         f.write(comment.id + "\n")

reddit = praw.Reddit("bot1")
bot_name = "UserInfo_Bot"
bot_profile = reddit.redditor(bot_name)

exclude_nsfw_string = "-nsfw"
test_subreddit = "PythonInfoBotTest"
call_word = "call userinfo_bot"

blacklisted_subs_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\blacklisted_subreddits.txt"
blacklisted_users_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\blacklisted_users.txt"
posts_replied_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\posts_replied.txt"
comments_replied_filename = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\comment_replied.txt"

reply_to_comment(reddit, test_subreddit, 5)
