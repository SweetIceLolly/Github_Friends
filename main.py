from data_processing import dig_followers, save_database, load_database, generate_diagram
from request import get_user_id, init_session
import datetime

if __name__ == '__main__':
    try:
        mode = int(input(
            "Select Mode:\n"                            \
            "1 = Draw diagram from database.npy\n"      \
            "2 = Generate database.npy from Github\n"   \
            "Anything else = Exit\n"
        ))
    except:
        exit(0)

    if mode == 1:
        load_database()
        print("Generating diagram...")
        generate_diagram(r'diagram.png')
        exit(0)
    elif mode == 2:
        print("First, I need your Github token.")
        print("Why? Check this out: https://developer.github.com/v3/#rate-limiting")
        print("To generate a token: https://github.com/settings/tokens")
        token_user = input("Username of the Token: ")
        token = input("Token: ")
        init_session(github_username=token_user, github_token=token)

        user = input("The user to query: ")
        user = user.strip()
        depth = int(input("Depth (Suggested: 1): "))
        user_id = get_user_id(user)
        print("User id of " + user + " is " + str(user_id))
        start_time = datetime.datetime.now()
        print(str(start_time) + " Digging started!")
        dig_followers(user_name=user, prev_id=user_id, depth=depth)
        print(str(datetime.datetime.now()) + " Digging finished!")
        print("Digging started at: " + str(start_time))
        save_database()
    else:
        print("See ya~")
