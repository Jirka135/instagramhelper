import re
import instaloader
import json
import time
from icecream import ic
import requests
import time

url_of_AI = f'http://localhost:5000/api/v1/generate'

def fetch_user_data(username_to_find, output_filename,stop_at):
    print(f"fetching data for user {username_to_find}")
    L = instaloader.Instaloader()
    L.load_session_from_file("aiarts69")
    time.sleep(30)
    try:
        profile = instaloader.Profile.from_username(L.context, username_to_find)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"User '{username_to_find}' does not exist on Instagram.")
        return
    
    user_data = {
        "user_profile_info": {
            "follower_count": profile.followers,
            "following_count": profile.followees,
            "users_bio": profile.biography
        },
        "user_posts": []
    }
    post_count = 0
    try:
        for post in profile.get_posts():
            if post_count < stop_at:
                post_data = {
                    "post_url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "post_likes": post.likes,
                    "post_comments": post.comments,
                    "post_caption": post.caption,
                    "hashtags": post.caption_hashtags,
                    "mentions": post.caption_mentions,
                    "date_of_release": str(post.date), 
                    "location": post.location
                }
                user_data["user_posts"].append(post_data)
                post_count += 1
                print(f"post_count: {post_count}")
            else:
                break
    except:
        print("no more posts on profile")
    if output_filename == "":
        output_filename = f"ig_accounts/{username_to_find}_instagram_data.json"
    with open(output_filename, "w", encoding="utf-8") as json_file:
        json.dump(user_data, json_file, ensure_ascii=False, indent=4)

    prepare_and_get_ai_help(output_filename)
    print(f"Data for user '{username_to_find}' has been saved to '{output_filename}'.")

def prepare_and_get_ai_help(output_filename):
    if output_filename == "":
        json_file_path = "training_jsons/" + output_filename
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        formatted_data = re.sub(r'[{}"\[\],]', '', json.dumps(data, indent=4))
    
    user_input = """
    
    I have a file containing data about my Instagram account, including information about my followers, following count, user bio, and a list of recent posts. I would like your assistance in analyzing and optimizing my Instagram presence based on this data.

    You can expect to find the following information in the JSON file:

    1. `user_profile_info`: Contains data about my Instagram profile, including follower count, following count, and user bio. Just tell me if i have nice follower count or not and how improve my followers, maybe suggest me better bio or something that is missing in my bio.

    2. `user_posts`: A list of recent posts, each with the following properties:
    - `post_url`: The URL of the Instagram post. - ignore this just use it as wariable to tell me which post we are talking about.
    - `post_likes`: The number of likes on the post. - at the end you can tell me which post have most of like and count all likes i got on my account.
    - `post_comments`: The number of comments on the post. here you can suggest to use some techniques to improve comment count , also tell me which post have most comments and all comments.
    - `post_caption`: The caption of the post. -  here you can suggest that i should use longer or shorter captions, also you can tell me that i can use more informative captions.
    - `hashtags`: An array of hashtags used in the post's caption. - here you can suggest to use more relevant hashtags (look at captions and try tu guess what is post about if possible), you can also tell me to use more or less hashtags
    - `mentions`: An array of mentions (other users or accounts) mentioned in the post's caption. - here you can tell me that i should cooperate with more accounts (but only if like less than 1/3 of my posts dont have any mentions)
    - `date_of_release`: The date and time when the post was published. -  here you can tell that i should post more frequently or less frequently and suggest me some some days i should post more frequently
    - `location`: The location where the post was taken (if available). - if i dont use location (its empty) suggest me to use it more (but only if i dont have location on at least 1/10 of my posts)

    I'm looking for insights and recommendations on how to improve my Instagram account. This may include suggestions for optimizing my user bio, using hashtags effectively, increasing engagement, or any other strategies to enhance my Instagram presence.

    Please analyze the data and provide actionable advice to help me grow my Instagram account. Thank you!
    
    at end of statement please show me my most liked posts and my most used hashtags also some helpful information.

    here is the data from my instagram account:

    put all information into one message please , make it as detailed as possible dont forget to include recomendation and also some usefull stats u get from my account.

    """ + formatted_data
    Comunicate_AI(user_input)

#debug function , hardcoded
def fetch_list_of_users(filename):
    user_list = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        if line.endswith("\n"):
            user_list.append(line[:-1])
    print(user_list)
    for user in user_list:
        user = user
        output_filename = f"training_jsons/{user}_instagram_data.json"
        fetch_user_data(user, output_filename,12)

def Comunicate_AI(prompt):
    request = {
        'prompt': prompt,
        'max_new_tokens': 2048,
        'auto_max_new_tokens': False,
        'max_tokens_second': 0,
        'seed': 1165095324,
    }

    # because im lazy im using same seed over and over again because some seed dont work at all and return empty values (i would need to train my model to make it work)
    # usefull seeds 1165095324, 220312723

    response = requests.post(url_of_AI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        #print(prompt + result)
        print(result)
    else:
        ic(response.status_code)

#this is just so... that i can make my life easier when copiing files from internet lists of famous people on instagram.
def filter_instagram_names(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            if line.strip().startswith("@"):
                line = line
                file.write(line[1:])
            else:
                continue

if __name__ == "__main__":


    username_to_find = input("Enter the Instagram username: ")
    #this code is ugly... ik if you want to make UI just remove calling one function from another and make it look cooler :D i won't do taht for now...
    fetch_user_data(username_to_find,"",12)
