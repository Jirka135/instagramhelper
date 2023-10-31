import instaloader
import json
import time
from icecream import ic
import html
import json
import requests
import time

url_of_AI = f'http://localhost:5000/api/v1/generate'

def fetch_user_data(username_to_find, output_filename):
    print(f"fetching data for user {username_to_find}")
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
    stop_at = 12
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
        print("ajaj chyba")
    with open(output_filename, "w", encoding="utf-8") as json_file:
        json.dump(user_data, json_file, ensure_ascii=False, indent=4)

    print(f"Data for user '{username_to_find}' has been saved to '{output_filename}'.")

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
        fetch_user_data(user, output_filename)

def Comunicate_AI(prompt):
    request = {
        'prompt': prompt,
        'max_new_tokens': 250,
        'auto_max_new_tokens': False,
        'max_tokens_second': 0,

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.7,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'additive_repetition_penalty': 0,
        'repetition_penalty_range': 0,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'grammar_string': '',
        'guidance_scale': 1,
        'negative_prompt': '',

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'custom_token_bans': '',
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(url_of_AI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        print(prompt + result)
    else:
        ic(response.status_code)

def create_training_json(name_of_folder):
    None

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

    L = instaloader.Instaloader()
    L.load_session_from_file("aiarts69")
    time.sleep(10)
    fetch_list_of_users("instagram_users_to_fetch.txt")


    #username_to_find = "josef.jindra.666"
    

    #fetch_list_of_users("instagram_users_to_fetch.txt")
    #with open("instagram_users_to_fetch.txt", "w", encoding="utf-8")

    #username_to_find = input("Enter the Instagram username: ")
    
    #filter_instagram_names("instagram_users_to_fetch.txt")
    #create_training_json()
    #user_input = "how to make dumplings"

    #Comunicate_AI(user_input)

    #user_input = input('Please enter question: ')