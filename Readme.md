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
/get <number> | Get the given number emails' literatures
