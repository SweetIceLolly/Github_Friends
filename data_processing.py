# For database storage
import numpy

# For github requests
from request import get_user_followers, get_user_following

# For diagram
from diagram import save_diagram

# {id1:[name, {follower1_id:name, follower2_id:name, ...}, {following1_id:name, following2_id:name, ...}], id2:...}
database = {}


def save_database():
    try:
        numpy.save("database.npy", database)
        print("database.npy saved!")
    except:
        print("Failed to save database.npy!")


def load_database():
    global database
    try:
        database = numpy.load("database.npy", allow_pickle=True).item()
        print("database.npy loaded!")
    except:
        print("Failed to load database.npy!")


def generate_diagram(path):
    global database
    save_diagram(path=path, database=database)


def dig_followers(user_name, prev_id, depth, curr_depth=0):
    print(" [#" + str(len(database)) + "] " + "    " * curr_depth + user_name)
    if curr_depth == 0:
        database[prev_id] = [user_name, {}, {}]
    if curr_depth > depth:
        return None

    follower = get_user_followers(user=user_name)
    if follower is None:
        return None
    following = get_user_following(user=user_name)
    if following is None:
        return None

    for entry in follower:
        entry_id = entry['id']
        entry_name = entry['login']

        if entry_id not in database:
            database[entry_id] = [entry_name, {}, {}]

        database[prev_id][1][entry_id] = entry_name
        dig_followers(
            user_name=entry_name,
            prev_id=entry_id,
            depth=depth,
            curr_depth=curr_depth + 1
        )

    for entry in following:
        entry_id = entry['id']
        entry_name = entry['login']

        if entry_id not in database:
            database[entry_id] = [entry_name, {}, {}]
        database[prev_id][2][entry_id] = entry_name
        dig_followers(
            user_name=entry_name,
            prev_id=entry_id,
            depth=depth,
            curr_depth=curr_depth + 1
        )
