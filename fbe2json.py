#!/bin/env python3
import argparse
from bs4 import BeautifulSoup
import os
import sys
import json

def parse_friends_htm(file_path):
    """
    Parses the friends.htm file and extracts the Facebook user name and categorized lists.

    Args:
        file_path (str): Path to the friends.htm file.

    Returns:
        dict: A dictionary containing the user name and categories with their items.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, 'lxml')  # You can use 'html.parser' if 'lxml' is not installed

    # Find the first <div class="contents">
    contents_div = soup.find('div', class_='contents')
    if not contents_div:
        print("Error: <div class='contents'> not found in the HTML file.")
        sys.exit(1)

    # Extract the <h1> text
    h1_tag = contents_div.find('h1')
    user_name = h1_tag.get_text(strip=True) if h1_tag else "Name Not Found"

    # Initialize a dictionary to hold categories and their items
    data = {
        "User": user_name,
        "Categories": {}
    }

    # Find all <h2> tags within the contents_div
    h2_tags = contents_div.find_all('h2')
    for h2 in h2_tags:
        category_name = h2.get_text(strip=True)
        # The <ul> is expected to be the next sibling after <h2>
        ul = h2.find_next_sibling('ul')
        if ul:
            # Extract all <li> items within the <ul>
            items = [li.get_text(strip=True) for li in ul.find_all('li')]
            data["Categories"][category_name] = items
        else:
            data["Categories"][category_name] = []

    return data
def parse_photos_htm(file_path):
    """
    Parses the photos.htm file and extracts the Facebook user name and categorized lists.

    Args:
        file_path (str): Path to the photos.htm file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
def parse_videos_htm(file_path):
    """
    Parses the videos.htm file and extracts the Facebook user name and categorized lists.

    Args:
        file_path (str): Path to the videos.htm file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

def parse_messages_htm(file_path):
    """
    Parses the messages.htm file and extracts the Facebook user name and categorized lists.

    Args:
        file_path (str): Path to the messages.htm file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract the user from the first <h1> inside .contents
    contents_div = soup.find("div", class_="contents")
    if not contents_div:
        print("Error: Could not find 'contents' div in the file.")
        sys.exit(1)
    
    user = contents_div.find("h1").text.strip() if contents_div.find("h1") else "Unknown User"
    
    # Extract all threads
    threads = []
    thread_divs = contents_div.find_all("div", class_="thread")
    
    for thread in thread_divs:
        # The conversation participants (text before the first .message div)
        between = thread.find(text=True, recursive=False).strip().replace("\n", "")
        
        messages = []
        p_divs = thread.find_all("p")
        for p_div in p_divs:
            # Extract user, datetime, and message text
            user_div = p_div.find_previous_sibling("div").find("div").find("span", class_="user")
            datetime_div = p_div.find_previous_sibling("div").find("div").find("span", class_="meta")
            message_p = p_div
            
            if user_div and datetime_div and message_p:
                message_data = {
                    "user": user_div.text.strip().replace("\n", ""),
                    "datetime": datetime_div.text.strip().replace("\n", ""),
                    "message": message_p.text.strip().replace("\n", "")
                }
                messages.append(message_data)
        
        threads.append({
            "between": between,
            "messages": messages
        })
    
    output_data = {
        "user": user,
        "threads": threads
    }
    
    return output_data
def parse_pokes_htm(file_path):
    """
    Parses the pokes.htm file and extracts the Facebook user name and categorized lists.

    Args:
        file_path (str): Path to the pokes.htm file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()


def parse_timeline_htm(file_path):
    """
    Parses the timeline.htm file and extracts the Facebook user name and post details.

    Args:
        file_path (str): Path to the timeline.htm file.

    Returns:
        dict: A dictionary containing the user name and list of posts with datetime and post content.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')  # You can use 'html.parser' if 'lxml' is not installed

    # Find the first <div class="contents">
    contents_div = soup.find('div', class_='contents')
    if not contents_div:
        print("Error: <div class='contents'> not found in the HTML file.")
        sys.exit(1)

    # Extract the <h1> text for the user name
    h1_tag = contents_div.find('h1')
    user_name = h1_tag.get_text(strip=True) if h1_tag else "Name Not Found"

    # Initialize a dictionary to hold the user and posts
    data = {
        "User": user_name,
        "Posts": []
    }

    # Find all <p> tags within the contents_div's <div>
    main_div = contents_div.find('div')

    if not main_div:
        print("Error: <div> containing <p> tags not found inside <div class='contents'>.")
        sys.exit(1)

    p_tags = main_div.find_all('p')
    for p in p_tags:
        meta_div = p.find('div', class_='meta')
        comment_div = p.find('div', class_='comment')
        # Skip if <div class="comment"> is missing
        if not comment_div:
            continue

        datetime_text = meta_div.get_text(strip=True) if meta_div else "No DateTime Found"
        post_text = comment_div.get_text(strip=True) if comment_div else "No Post Content"

        # Append the post to the data dictionary
        data["Posts"].append({
            "datetime": datetime_text,
            "post": post_text
        })

    return data
        
def parse_events_htm(file_path):
    """
    Parses the events.htm file and extracts the Facebook user name and categorized lists.

    Args:
        file_path (str): Path to the events.htm file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
def parse_security_htm(file_path):
    """
    Parses the security.htm file and extracts the Facebook user name and categorized lists.

    Args:
        file_path (str): Path to the security.htm file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

def parse_ads_htm(file_path):
    """
    Parses the ads.htm file and extracts the Facebook user name and categorized lists.

    Args:
        file_path (str): Path to the ads.htm file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

def parse_mobile_devices_htm(file_path):
    """
    Parses the mobile_devices.htm file and extracts the Facebook user name and categorized lists.

    Args:
        file_path (str): Path to the mobile_devices.htm file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

def parse_places_htm(file_path):
    """
    Parses the places.htm file and extracts the Facebook user name and categorized lists.

    Args:
        file_path (str): Path to the places.htm file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
def parse_survey_responses_htm(file_path):
    """
    Parses the survey_responses.htm file and extracts the Facebook user name and categorized lists.

    Args:
        file_path (str): Path to the survey_responses.htm file.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Parse Facebook export files and convert to JSON.")
    parser.add_argument('--friends', required=False, help="Path to the friends.htm file.")
    parser.add_argument('--photos', required=False, help="Path to the photos.htm file.")
    parser.add_argument('--videos', required=False, help="Path to the videos.htm file.")
    parser.add_argument('--messages', required=False, help="Path to the messages.htm file.")
    parser.add_argument('--max-threads', required=False, help="Maximum number of threads to output.")
    parser.add_argument('--offset', required=False, help="Number of threads to offset by.")
    parser.add_argument('--pokes', required=False, help="Path to the pokes.htm file.")
    parser.add_argument('--timeline', required=False, help="Path to the timeline.htm file.")
    parser.add_argument('--events', required=False, help="Path to the events.htm file.")
    parser.add_argument('--security', required=False, help="Path to the security.htm file.")
    parser.add_argument('--ads', required=False, help="Path to the ads.htm file.")
    parser.add_argument('--mobile_devices', required=False, help="Path to the mobile_devices.htm file.")
    parser.add_argument('--places', required=False, help="Path to the places.htm file.")
    parser.add_argument('--survey_responses', required=False, help="Path to the survey_responses.htm file.")

    args = parser.parse_args()
    if args.friends is not None:
        file_path = args.friends
        # Parse the friends.htm file
        parsed_data = parse_friends_htm(file_path)
    elif args.photos is not None:
        file_path = args.photos
        # Parse the photos.htm file
        parsed_data = parse_photos_htm(file_path)
    elif args.videos is not None:
        file_path = args.videos
        # Parse the videos.htm file
        parsed_data = parse_videos_htm(file_path)
    elif args.messages is not None:
        file_path = args.messages
        # Parse the messages.htm file
        messages = parse_messages_htm(file_path)
        threads = messages["threads"]
        if args.max_threads is not None:
            limit = args.max_threads
            if limit > len(threads):
                limit = len(threads)
            threads = threads[:limit]
        if args.offset is not None:
            if args.offset is not None and args.max_threads is not None:
                limit = args.offset + args.max_threads
                if limit > len(threads):
                    limit = len(threads)
                threads = threads[args.offset:limit]
            else:
                threads = threads[args.offset:]
        parsed_data = {
            "user": messages["user"],
            "threads": threads
        }

    elif args.pokes is not None:
        file_path = args.pokes
        # Parse the pokes.htm file
        parsed_data = parse_pokes_htm(file_path)
    elif args.timeline is not None:
        file_path = args.timeline
        # Parse the timeline.htm file
        parsed_data = parse_timeline_htm(file_path)
    elif args.events is not None:
        file_path = args.events
        # Parse the events.htm file
        parsed_data = parse_events_htm(file_path)
    elif args.security is not None:
        file_path = args.security
        # Parse the security.htm file
        parsed_data = parse_security_htm(file_path)
    elif args.ads is not None:
        file_path = args.ads
        # Parse the ads.htm file
        parsed_data = parse_ads_htm(file_path)
    elif args.mobile_devices is not None:
        file_path = args.mobile_devices
        # Parse the mobile_devices.htm file
        parsed_data = parse_mobile_devices_htm(file_path)
    elif args.places is not None:
        file_path = args.places
        # Parse the places.htm file
        parsed_data = parse_places_htm(file_path)
    elif args.survey_responses is not None:
        file_path = args.survey_responses
        # Parse the survey_responses.htm file
        parsed_data = parse_survey_responses_htm(file_path)
    else:
        print("No valid file path provided.")
        sys.exit(1)
    # Output the parsed data as JSON (you can change this to other formats if needed)
    print(json.dumps(parsed_data, indent=4))

if __name__ == "__main__":
    main()