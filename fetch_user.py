"""
Usage: fetch_user <query>  [options]

Fetch a list of targets from Twitter API.

Options:
  -h --help                    Show this screen.
  --stop-on-rate-limit         Stop fetching and export the graph when a rate limit is raised.
  --credentials <file>         Path of the credentials for Twitter API [default: credentials.json].
  --excluded <file>            Path of the list of excluded users [default: excluded.json].
"""

import requests
import twitter
import json
from docopt import docopt
from pathlib import Path
from fetch_data import fetch_users

def main():
    options = docopt(__doc__)
    credentials = json.loads(open(options["--credentials"]).read())
    apis = [
        twitter.Api(consumer_key=credential["api_key"],
                    consumer_secret=credential["api_secret_key"],
                    access_token_key=credential["access_token"],
                    access_token_secret=credential["access_token_secret"],
                    sleep_on_rate_limit=False)
        for credential in credentials
    ]

    try:
        search_query = options["<query>"].split(',')
        for target in search_query:
            print("Process query {}".format(target))
            followers, friends, mutuals, all_users = fetch_users(apis, target, True, 'all', 0, Path('out'))

            users = { user["id"] : user for user in all_users }

            for i in mutuals:
                user = users[i]
                print(f"{user['name']} (@{user['screen_name']})")
            print(len(mutuals))    
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        print(e)  # Why do I get these?
        main()  # Retry!

if __name__ == "__main__":
    main()
