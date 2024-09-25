import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for LeetCode problems
LEETCODE_PROBLEMS_URL = "https://leetcode.com/problemset/all/"

# Headers to make the request look like it's coming from a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to get the HTML content of the page
def get_page_content(url):
    response = requests.get(url, headers=HEADERS)  # Pass the headers here
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve content: {response.status_code}")
        return None

# Function to parse the LeetCode problems from the HTML content
def parse_problems(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the problem list table
    problem_rows = soup.find_all('tr', {'class': 'reactable-data-row'})

    problems = []
    for row in problem_rows:
        problem = {}
        
        # Problem name and URL
        name_col = row.find('a', {'href': True})
        problem['name'] = name_col.text.strip()
        problem['url'] = 'https://leetcode.com' + name_col['href']
        
        # Problem difficulty
        difficulty_col = row.find_all('td')[-1]  # Last column contains the difficulty
        problem['difficulty'] = difficulty_col.text.strip()
        
        problems.append(problem)

    return problems

# Function to scrape all problems
def scrape_leetcode_problems():
    html_content = get_page_content(LEETCODE_PROBLEMS_URL)
    if html_content:
        problems = parse_problems(html_content)
        return problems
    return []

# Function to create a dataset from scraped problems
def create_problems_dataset(problems):
    df = pd.DataFrame(problems)
    df.to_csv("leetcode_problems.csv", index=False)
    print(f"Dataset created with {len(problems)} problems.")

# Main script
if __name__ == "__main__":
    problems = scrape_leetcode_problems()
    if problems:
        create_problems_dataset(problems)
    else:
        print("No problems found.")
