from playwright.sync_api import sync_playwright, TimeoutError
from creds import username, password
import os
import time
import datetime

PATH = os.path.abspath(os.path.dirname(__file__))
twitter = 'https://twitter.com/'
follower_link = '/followers'
following_link = '/following'
primaryColumn = 'div[data-testid="primaryColumn"]'
userCell = 'div[data-testid="UserCell"]'

def getNowTrue():
    return datetime.datetime.now()

def twit_init():
    dir_contents = os.listdir(PATH)
    if 'state.json' not in dir_contents:
        print('State not found...')
        with sync_playwright() as p:
            browser = p.chromium.launch()
            # browser = p.chromium.launch(headless=False, slow_mo=500)
            context = browser.new_context()
            page = context.new_page()
            page.goto('https://twitter.com/login')
            login_field = page.get_by_text('username')
            login_field.fill(username)
            next_button = page.get_by_text('Next').click()
            password_field = page.get_by_text('Password').nth(1)
            password_field.fill(password)
            login_button = page.get_by_text('Log in').click()
            store_state = context.storage_state(path=PATH+'/state.json')
    else:
        print('State found...')

def new_follower_count(page, followers=[]):
    while True:
        try:
            userCell_count = page.locator(primaryColumn).locator(userCell).count()
            new_followers = []
            page.mouse.wheel(delta_x=0, delta_y=1000)
            for i in range(userCell_count):
                follower = page.locator(primaryColumn).locator(userCell).nth(i).locator('a').nth(2).inner_text()
                print(follower)
                new_followers.append(follower)
            print(f'Found {len(new_followers)} followers, adding to list...')
            seen_followers = len(followers)
            for new_follower in new_followers:
                if new_follower not in followers:
                    followers.append(new_follower)
            total_followers = len(followers)
            print(f'Total followers: {total_followers}')
            new_followers = total_followers-seen_followers
            break
        except TimeoutError:
            continue
    return new_followers

def get_followers(target_user, follows):
    followers = []
    if follows == True:
        follows_link = follower_link
    elif follows == False:
        follows_link = following_link
    target_site = twitter+target_user+follows_link
    twit_init()
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False, slow_mo=100)
        print('Twitter spider is loading all the things..')
        browser = p.chromium.launch()
        context = browser.new_context(storage_state=PATH+'/state.json')
        page = context.new_page()
        print('Spider has loaded context, starting to crawl...')
        page.goto(target_site)
        page.wait_for_load_state('networkidle')
        while True:
            new_followers = new_follower_count(page, followers)
            if new_followers == 0:
                break
    followers = [i[1:] for i in followers]
    return followers
