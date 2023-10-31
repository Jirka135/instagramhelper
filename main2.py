import requests
from bs4 import BeautifulSoup

# Replace this URL with the one you want to fetch
url = 'https://instagram.com/josef.jindra.666'

try:
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the HTML content of the page
        html_content = response.text

        # Create a BeautifulSoup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find specific data in the HTML using BeautifulSoup methods
        # For example, finding and printing the title of the page:
        title = soup.find('title')
        if title:
            print("Title:", title.text)

        # You can find other elements and data in a similar way

    else:
        print(f'Failed to retrieve the web page. Status code: {response.status_code}')

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')