import json
from pathlib import Path

def getUsers(user, kind):
    path = Path(f"out/{user}/cache/{kind}.json")

    with path.open("r") as f:
        data = json.load(f)
        return { user["id"] : user for user in data }

def getAll(user):
    friends = getUsers(user, 'friends')
    followers = getUsers(user, 'followers')
    mutuals = set(friends.keys()).intersection(followers.keys())

    return friends, followers, mutuals

def getIngroup(core):
    friends, _, ingroup = getAll(core[0])

    for acct in core[1:]:
        _, _, mutuals = getAll(acct)
        ingroup = ingroup.intersection(mutuals)

    return friends, ingroup

core = ['eigenrobot', 'liminal_warmth', 'visakanv']
friends, ingroup = getIngroup(core)

print("# ingroup seeds")
for screen in core:
    print(f"1. [@{screen}](https://twitter.com/{screen})")

print()
print("# ingroup")
for i in ingroup:
    friend = friends[i]
    name = friend['name']
    screen = friend['screen_name']
    print(f"1. {name} ([@{screen}](https://twitter.com/{screen}))")
