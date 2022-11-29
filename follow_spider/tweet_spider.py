from tweet_toolbox import get_followers, getNowTrue
from tweet_config import user_bot, follow_bot

target = input('Use this script at your own discretion... Please enter the twitter handle:')

def follow_bot_maker(follower, target_neo):
    merge_follower = follow_bot.create_or_update({'twitter_id':f'{follower}', 'last_checked':getNowTrue()})
    follower_bot = follow_bot.nodes.get(twitter_id=follower)
    check_rel = follower_bot.twit_follow.relationship(target_neo)
    if check_rel == None:
        follower_bot.twit_follow.connect(target_neo)
    else:
        check_rel.last_checked = getNowTrue()
        check_rel.save()

merge_target = user_bot.create_or_update({'twitter_id':f'{target}', 'last_checked':getNowTrue()})
target_neo = user_bot.nodes.get(twitter_id=target)
followers = get_followers(target, follows=True)

for follower in followers:
    follow_bot_maker(follower, target_neo)    

for follower in followers:
    followings = get_followers(follower, follows=False)
    for following in followings:
        merge_following = user_bot.create_or_update({'twitter_id':f'{following}', 'last_checked':getNowTrue()})
        following_neo = user_bot.nodes.get(twitter_id=following)
        follow_bot_maker(follower, following_neo)