from tweet_config import follow_bot, user_bot


a = user_bot.nodes
for i in a:
    if 100 > len(i.twit_follow) > 50:
        print(f'Twitter user {i.twitter_id} has {len(i.twit_follow)} followers in the botnet...')
