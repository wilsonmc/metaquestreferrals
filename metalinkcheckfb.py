import requests
import re
from tqdm import tqdm

def extract_data(url):
    try:
        # Fetch the HTML content of the webpage
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()

        # Extract appname and overall_rating using regex
        html_content = response.text

        # Use regular expressions to find the values after "appName" and "overall_rating"
        appname_match = re.search(r'"appName"\s*:\s*"([^"]+)"', html_content)
        overall_rating_match = re.search(r'"overall_rating"\s*:\s*([^,}\]]+)', html_content)

        # Search for "Get 25% off" in the HTML source
        get_25_off_found = "Get 25% off" in html_content

        # Collect the data
        if appname_match:
            appname = appname_match.group(1)
            if overall_rating_match:
                overall_rating = overall_rating_match.group(1)
                result = f"{appname} ({overall_rating}⭐)"
            else:
                result = appname

            # Add exclamation mark if "Get 25% off" is not found
            result = f"!{result}" if not get_25_off_found else result

            data = (appname, result, url)
            return data
        else:
            print(f"Unable to find appName in {url}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error processing {url}: {e}")
        return None

def main():
    # Read the list of URLs from the file
    with open('urls.txt', 'r') as file:
        urls = file.read().splitlines()

    # Create a progress bar
    with tqdm(total=len(urls), desc="Checking links", unit="link") as progress_bar:
        # Collect the data for each URL
        data_list = []
        for url in urls:
            data = extract_data(url)
            data_list.append(data)
            progress_bar.update(1)

    # Sort the data by appname
    sorted_data = sorted(filter(None, data_list), key=lambda x: x[0])

    # Print the sorted results
    for appname, result, url in sorted_data:
        print(result)
        print(url)
        print("-" * 30)

if __name__ == "__main__":
    main()
