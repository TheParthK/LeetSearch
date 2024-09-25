from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# Path to your ChromeDriver
CHROME_DRIVER_PATH = '/path/to/chromedriver'

# Function to initialize the Selenium WebDriver
def init_driver():
    service = Service(executable_path=CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run browser in headless mode (optional)
    driver = webdriver.Chrome(service=service, options=options)  # Use service here
    return driver

# Function to scrape the LeetCode problems using Selenium
def scrape_leetcode_problems():
    driver = init_driver()
    driver.get("https://leetcode.com/problemset/all/")
    
    # Wait for the page to load
    time.sleep(5)
    
    # Get page content and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

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
