import argparse
import requests
from bs4 import BeautifulSoup
import re
from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Check if '25%' is in the title of web pages.")
    parser.add_argument('--linebreak', '--lb', action='store_true', help='Add line breaks after each response.')
    parser.add_argument('--date', action='store_true', help='Add current date and time after "25% off CONFIRMED" text.')
    return parser.parse_args()

# Read the URLs from the 'urls.txt' file
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines()]

def print_colored(text, color_code):
    print(f"{color_code}{text}{Style.RESET_ALL}", end='')

args = parse_arguments()

try:
    for url in urls:
        # Fetch the HTML content of the page
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            html_content = response.text

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Check if the word "25%" exists in the title of the page
            title = soup.title.text.lower() if soup.title else ""
            if "25%" in title:
                # Extract text after "appName":" up to the following , character
                match = re.search(r'"appName":\s*"(.*?)"', html_content)
                if match:
                    extracted_text = match.group(1)
                    print_colored(f"25% off CONFIRMED for {extracted_text} -", Fore.GREEN)
                    # Add current date and time if --date argument is used
                    if args.date:
                        date_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print_colored(f" {date_text}", Fore.LIGHTBLUE_EX)
                    else:
                        print()  # Add a newline if --date argument is not used
                else:
                    print_colored(f"No match found for 'appName' in the page -", Fore.GREEN)
            else:
                print_colored(f"25% off is NOT available for this page -", Fore.RED)
            
            # Print the URL without color on the same line
            print_colored(f" URL: {url}", Fore.WHITE)  # Specify the color explicitly

            # Add line break if the --linebreak or --lb argument is provided
            if args.linebreak:
                print()

        else:
            print_colored(f"Failed to retrieve the page. Status code: {response.status_code} -", Fore.RED)
            
            # Print the URL without color on the same line
            print_colored(f" URL: {url}", Fore.WHITE)  # Specify the color explicitly

            # Add line break if the --linebreak or --lb argument is provided
            if args.linebreak:
                print()

except requests.exceptions.RequestException as e:
    print_colored(f"An error occurred: {e}", Fore.RED)
    
    # Add line break if the --linebreak or --lb argument is provided
    if args.linebreak:
        print()
