# Udemy Course Finder Bot | Udemy Kupon Bulucu Botu
This bot finds new udemy coupons and sends to the channel.

# Before Setup
- You must have `python >= 3.6`
- You need to install `discord.py`, `beautifulsoup4` & `datagoose`

# Setup
- config.json
    - Enter your bot token to the `token`.
    - This bot doesn't have any command but if you will add something, you can set prefix from `prefix`.
    - Channels
        - This bot only supports `turkish` & `english` language. But you can add new languages easily. [`tr` => `turkish`, `en` => `english`]
        - Add your channel ids to the `channel`
    - Ping
        - Ping is the ping role when coupon found.

# Running
You just can start with `python main.py`.