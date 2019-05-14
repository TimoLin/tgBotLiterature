tgBotLiterature
===============
Your Telegram literature tracking bot.

# How does it work?  
This bot combines __Google Scholar Alert__ (sent to Gmail) and __Telegram bot__ to let you track and orgonize literatures without leaving Telegram.  
It converts your Google Scholar Alert emails to Telegram messages: one literature to one message. If you don't like this one, just delete it in the chat.  
![img](https://i.imgur.com/7Q6bxjY.jpg)

# What do we need?  
1. Gmail API
2. Telegram bot
3. python3

# How to run? 
## Install
### Prerequisites for Pi
```shell
sudo apt install gcc libffi-dev libssl-dev python3-dev
```
### Pip packages
```shell
pip3 install requirements.txt
```
## Config.ini  
Change token info to your own Telegram bot's token.  
If you are using proxy to connect Telegram, change it to your own.   
Also,you need create a `label` in `Gmail` to filter the `Google Scholar Alert` emails. Once you have done that, change the label name to your own.
```
[token_info]
token = 123456789:ABCDEFGH_ijklmnopqrstuvwxyzabcdefgh

[proxy_info]
#proxy = socks5://127.0.0.1:1080/
proxy = 

[label_name]
label = LITER
```

## On a computer, a Raspberry Pi or a VPS  
```shell  
python3 tgbot.py
```  
## In your telegram  
Command | Description   
:----:  | :----: 
/start  | Show welcome message
/latest | Get the latest email's literatures
/all    | Get all the literatures
/get \<number\> | Get the given number emails' literatures

# Literature message  
The message has been formatted using Markdown. Like follows:

[Title]()  
__Author1, Author2... - Journal of Sth, Year__  
Abstract: blah blah  

The title has a hyper link pointing the paper's website.  
The authors, journal and year are bold.  
The abstract is plain text.  

Example message:  
[A Computational Study on Laminar Flame Propagation in Mixtures with Non-Zero Reaction Progress](http://scholar.google.com/scholar_url?url=https://www.researchgate.net/profile/Peng_Zhao23/publication/331966184_Computational_Study_on_Laminar_Flame_Propagation_in_Mixtures_with_Non-Zero_Reaction_Progress/links/5c95957c299bf11169409dc4/Computational-Study-on-Laminar-Flame-Propagation-in-Mixtures-with-Non-Zero-Reaction-Progress.pdf&hl=en&sa=X&d=17953251988986958219&scisig=AAGBfm2VkBWAGKGHhcuWnP2Mnvew_e9aaw&nossl=1&oi=scholaralrt&hist=SL5peagAAAAJ:1186450557092380684:AAGBfm1triiJcRjc6dSTGpiDbjKZ23AzMw)  
__H Lin, P Zhao, H Ge - SAE Technical Paper, 2019__  
… turbulent premixed flames. Experimentally, laminar flame speed can be measured using different apparatus, including the coun- terflow twin flame, spherical combustion bomb, Bunsen flame, and flat flame, etc. 1, 2, 3, 4. A …  


