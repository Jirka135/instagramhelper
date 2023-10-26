import instaloader
import json
import time
from icecream import ic
import html
import json
import requests



HOST = ''
URI = f'http://localhost:5000/api/v1/generate'

def fetch_user_data(username_to_find, output_filename):
    L = instaloader.Instaloader()
    
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
    for post in profile.get_posts():
        time.sleep(0.1)
        post_data = {
            "post_url": f"https://www.instagram.com/p/{post.shortcode}/",
            "post_likes": post.likes,
            "post_comments": post.comments,
            "post_caption": post.caption,
            "hashtags": post.caption_hashtags,
            "mentions": post.caption_mentions,
            "date_of_release": str(post.date), 
            "location": post.location,
            "mentions": post.caption_mentions
        }
        user_data["user_posts"].append(post_data)
        post_count += 1
        ic(post_count)
    with open(output_filename, "w", encoding="utf-8") as json_file:
        json.dump(user_data, json_file, ensure_ascii=False, indent=4)
    
    print(f"Data for user '{username_to_find}' has been saved to '{output_filename}'.")

def main():
    #username_to_find = input("Enter the Instagram username: ")
    username_to_find = 'lego'
    output_filename = f"{username_to_find}_instagram_data.json"
    
    fetch_user_data(username_to_find, output_filename)

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

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        print(prompt + result)
    else:
        ic(response.status_code)

if __name__ == "__main__":
    #main()

    user_input = "how to make dumplings"

    Comunicate_AI(user_input)

    #user_input = input('Please enter question: ')