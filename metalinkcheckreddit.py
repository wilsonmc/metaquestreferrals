import argparse
import requests
from bs4 import BeautifulSoup
import re
from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Check if '25%' is in the title of web pages.")
    parser.add_argument('--date', action='store_true', help='Add the current date and time after "25% off" text.')
    parser.add_argument('--sort', action='store_true', help='Sort results by overall_rating.')
    parser.add_argument('--output', type=str, help='Specify the output file for the results.')
    parser.add_argument('--reddit', action='store_true', help='Use Reddit-specific markdown in the output.')
    return parser.parse_args()

def extract_json_value(json_string, key):
    match = re.search(fr'"{key}":\s*"?([\d.]+)"?', json_string)
    return match.group(1) if match else None

def extract_rating_count_string(html_content):
    match = re.search(r'"rating_count_string":\s*"([^"]+)"', html_content)
    return match.group(1) if match else None

def process_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.title.text.lower() if soup.title else ""
        if "25%" in title:
            match = re.search(r'"appName":\s*"(.*?)"', html_content)
            if match:
                extracted_text = match.group(1)

                overall_rating = extract_json_value(html_content, "overall_rating")
                rating_count_string = extract_rating_count_string(html_content)

                result = {
                    'url': url,
                    'app_name': extracted_text,
                    'overall_rating': float(overall_rating) if overall_rating else 0.0,
                    'rating_count': rating_count_string
                }

                return result

    return None

def print_colored(text, color_code):
    return f"{color_code}{text}{Style.RESET_ALL}"

def print_result(result, show_date, use_reddit_markdown):
    extracted_text = result['app_name']
    overall_rating = result['overall_rating']
    rating_count_string = result['rating_count']
    url = result['url']

    output = (
        f"{bold(extracted_text)}  \n" if use_reddit_markdown else
        f"{extracted_text}\n"
    )

    output += "25% off\n"  # No extra line break here
    if show_date:
        date_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output += f" checked on {date_text}\n"

    if use_reddit_markdown:
        output += (
            f"**Overall Rating:** {bold(overall_rating)}\n"
            f"Rating Count: {rating_count_string}\n"
            f"[{url}]({url})\n"
        )
    else:
        output += (
            f"Overall Rating: {overall_rating}\n"
            f"Rating Count: {rating_count_string}\n"
            f"LINK: {url}\n"
        )

    return output + '\n'  # Add a line break after each result

def bold(text):
    return f"**{text}**"

def main():
    args = parse_arguments()

    # Read the URLs from the 'urls.txt' file
    with open('urls.txt', 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    # Process URLs and store results
    results = []
    for url in urls:
        result = process_url(url)
        if result:
            results.append(result)

    # Sort results based on overall_score if --sort is provided
    if args.sort:
        results = sorted(results, key=lambda x: x['overall_rating'], reverse=True)

    # Print results with line breaks and write to the output file if specified
    with open(args.output, 'w') if args.output else None as output_file:
        for result in results:
            formatted_result = print_result(result, show_date=args.date, use_reddit_markdown=args.reddit)
            print(formatted_result)  # Print to console
            # Write to the output file if specified
            if output_file:
                # Strip ANSI escape codes before writing to the file
                output_file.write(re.sub(r'\x1b\[[0-9;]*m', '', formatted_result))

if __name__ == "__main__":
    main()
