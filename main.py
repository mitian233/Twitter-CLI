import os
import tweepy
import json
import argparse

parser = argparse.ArgumentParser(description='Twitter CLI')
parser.add_argument('-post', type=str, default=None, help='Text of the tweet you want to send. ')
parser.add_argument('-img', type=str, default=None, help='One image attached to your tweet (optional). ')
parser.add_argument('-tl', help='Get timeline', action='store_true')
parser.add_argument('-mo', help='Get montions timeline', action='store_true')
parser.add_argument('-delete', type=str, default=None, help='Provide a tweet id and del the tweet. ')
parser.add_argument('-reply', type=str, default=None, help='Provide a tweet id and reply to the tweet. ')
parser.add_argument('-like', type=str, default=None, help='Provide a tweet id and like the tweet. ')
args = parser.parse_args()
t_text = args.post
t_image = args.img
t_del = args.delete
t_reply = args.reply
t_like = args.like

# Proxy settings(optional)
#os.environ["http_proxy"] = "http://127.0.0.1:10809"
#os.environ["https_proxy"] = "http://127.0.0.1:10809"
# Proxy settings end

app_config_file = 'app.config.json'
user_config_file = 'user.config.json'

# Authentication
if not os.path.exists(app_config_file):
    print('Collect app key and secret')
    consumer_key = input('Consumer key of your application:')
    consumer_secret = input('Consumer secret of your application:')
    application_info = {'consumer_key': consumer_key, 'consumer_secret': consumer_secret}
    with open(app_config_file, 'w') as json_file:
        json.dump(application_info, json_file)
        json_file.close()
        print('Successfully linked to your app. ')
with open(app_config_file, 'r') as json_file:
    json_dict = json.load(json_file)
    consumer_key = json_dict['consumer_key']
    consumer_secret = json_dict['consumer_secret']
    json_file.close()

# print('Consumer key:\033[92m' + consumer_key + '\033[0m \nConsumer secret:\033[92m' + consumer_secret + '\033[0m')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback='oob')

if not os.path.exists(user_config_file):
    print('It seems that you are running this application for the first time. Let\'s creat a config file:')
    print('Authorization:' + auth.get_authorization_url(signin_with_twitter=True))
    verifier = input('Type the PIN code you got here:')
    access_token, access_token_secret = auth.get_access_token(verifier)
    userdata = {'access_token': access_token, 'access_token_secret': access_token_secret}
    with open(user_config_file, 'w') as json_file:
        json.dump(userdata, json_file)
        json_file.close()
        print('Successfully created config file. ')
with open(user_config_file, 'r') as json_file:
    json_dict = json.load(json_file)
    access_token = json_dict['access_token']
    access_token_secret = json_dict['access_token_secret']
    json_file.close()
# print('Access Token:\033[92m' + access_token + '\033[0m \nAccess Token secret:\033[92m' + access_token_secret + '\033[0m')
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# Authentication end

# Define functions
def show_my_timeline():
    public_tweets = api.home_timeline(trim_user='ture')
    for tweet in public_tweets:
        print(
            'Status id:\033[92m' + tweet.id_str + '\033[0m\n@' + tweet.user.screen_name + ':\n' + tweet.text + '\n===============')


def show_mentions_timeline():
    public_tweets = api.mentions_timeline()
    for tweet in public_tweets:
        print(
            'Status id:\033[92m' + tweet.id_str + '\033[0m\n@' + tweet.user.screen_name + ':\n' + tweet.text + '\n===============')


def return_newest_post_id():
    public_tweets = api.user_timeline(count=1, trim_user='ture')
    for tweets in public_tweets:
        return tweets.id_str


def reply_the_newest_mention(reply_text):
    public_tweets = api.mentions_timeline(count=1, trim_user='ture')
    for tweets in public_tweets:
        api.create_favorite(id=tweets.id)
        reply_text = '@' + tweets.user.screen_name + ' ' + reply_text
        api.update_status(status=reply_text, in_reply_to_status_id=tweets.id)


def reply_tweet(reply_text, tweet_id, img_path):
    public_tweet = api.get_status(id=tweet_id, trim_user='ture')
    reply_text = '@' + public_tweet.user.screen_name + ' ' + reply_text
    if img_path == None:
        api.update_status(status=reply_text, in_reply_to_status_id=tweet_id)
    else:
        api.update_status_with_media(filename=img_path, status=reply_text, in_reply_to_status_id=tweet_id)


# Functions definitions end

if args.tl:
    show_my_timeline()

if args.mo:
    show_mentions_timeline()

if not t_del == None:
    print('\033[31mDelete tweet\033[0m:\033[92m' + t_del + '\033[0m')
    api.destroy_status(t_del)

if not t_text == None:
    if t_image == None:
        api.update_status(t_text)
        if not t_reply == None:
            reply_tweet(t_text, t_reply, None)
        print('\033[92mInfo\033[0m:Tweet without images.\n\033[92mTweet ID\033[0m:' + return_newest_post_id())
    else:
        api.update_status_with_media(status=t_text, filename=t_image)
        if not t_reply == None:
            reply_tweet(t_text, t_reply, t_image)
        print('\033[92mInfo\033[0m:Tweet with images.\n\033[92mTweet ID\033[0m:' + return_newest_post_id())

if not t_like == None:
    print('\033[31mLike tweet\033[0m:\033[92m' + t_like + '\033[0m')
    api.create_favorite(id=t_like)
