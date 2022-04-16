# Twitter CLI
Post tweets (with one photo) in your command line! 

## Dependencies

```shell
pip install tweepy
```

## Support

- [x] Post tweets(with images)
- [x] Delete tweets
- [x] Show time line
- [x] Like tweets
- [x] Reply tweets
- [ ] Send Direct message
- [ ] Reply Direct message
- [ ] And more...

## Setup

1. This application does not provide existing twitter api, you need to [apply manually](https://developer.twitter.com/en/portal/).
2. After you successfully applied **Twitter API v1** access, please follow the prompts in the application output to create a configuration file. 
    - Application might read tweets and profile information, read and post direct messages. So you need to choose **Read and write and Direct message** in App permissions settings. 

## Usage

Use the following commands to get command help:

```shell
python main.py -h
```

### Proxy

Uncomment these lines and replace with your own. 

```python
# Proxy settings(optional)
import os
os.environ["http_proxy"] = "http_proxy"
os.environ["https_proxy"] = "http_proxy"
# Proxy settings end
```