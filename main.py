import os
import tweepy
import json
import argparse

parser = argparse.ArgumentParser(description='Twitter CLI')
parser.add_argument('-t', type=str, default=None, help='Text of the tweet you want to send. ')
parser.add_argument('-img', type=str, default=None, help='One image attached to your tweet (optional). ')
parser.add_argument('-delete', type=str, default=None, help='Provide a tweet id and del the tweet. ')
args = parser.parse_args()
t_text = args.t
t_image = args.img
t_del = args.delete

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


def reply_the_newest_mention(reply_text):
    public_tweets = api.mentions_timeline(count=1, trim_user='ture')
    for tweets in public_tweets:
        api.create_favorite(id=tweets.id)
        reply_text = '@' + tweets.user.screen_name + ' ' + reply_text
        api.update_status(status=reply_text, in_reply_to_status_id=tweets.id)


def post_tweet(text):
    api.update_status(text)


def post_tweet_with_media(text, media_file):
    api.update_status_with_media(status=text, filename=media_file)


def del_tweet(tweet_id):
    api.destroy_status(tweet_id)


# Functions definitions end

if t_text == None and t_del == None and t_image == None:
    print('\033[31mError\033[0m:Invalid input. ')
else:
    if not t_del == None:
        print('\033[31mDelete tweet\033[0m:\033[92m' + t_del + '\033[0m')
        del_tweet(t_del)
    else:
        if t_text == None:
            print('\033[31mError\033[0m:No Twitter contents')
            exit()
        else:
            if t_image == None:
                print('\033[92mInfo\033[0m:Tweet without images. ')
                post_tweet(t_text)
            else:
                print('\033[92mInfo\033[0m:Tweet with images. ')
                post_tweet_with_media(t_text, t_image)
