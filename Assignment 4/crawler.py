from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re 
from collections import deque
from urllib.parse import urljoin
import pymongo


class FacultyCrawler:
    def __init__(self, seed_url):
        self.seed_url = seed_url
        self.frontier = deque([seed_url])
        self.visited = set()
        self.target_url = None
    
    # Helper function to check if the page is the target page (Permanent Faculty page)
    def is_target(self, soup):
        title_tag = soup.find('title')
        if title_tag and title_tag.string:  
            return bool(re.search('Permanent Faculty', title_tag.string))
        return False
    
    # Q4 Crawl the website to find the target page
    def crawl_for_target(self):
        while self.frontier:
            url = self.frontier.popleft()
            self.visited.add(url)
            print("Crawling:", url)
            try:
                with urlopen(url) as response:
                    html_content = response.read()
                    soup = BeautifulSoup(html_content, 'html.parser')

                    if self.is_target(soup):
                        print("Target found:", url)
                        self.target_url = url
                        return url

                    for link in soup.find_all('a', href=True):
                        abs_link = urljoin(url, link['href'])

                        if abs_link not in self.visited:
                            self.frontier.append(abs_link)
                            self.visited.add(abs_link)
            except (HTTPError, URLError) as e:
                print("Failed to access:", url)
                continue

        print("Target not found.")
        return None

    # Q5 Parse the faculty data from the target page    
    def crawl_for_faculty(self):
        with urlopen(self.target_url) as response:
            html_content = response.read()
            soup = BeautifulSoup(html_content, 'html.parser')

        faculty_list = []

        for raw_faculty in soup.find_all('div', class_='clearfix'):
            faculty_data = {}
            name = raw_faculty.find('h2')
            
            if not name:
                continue
            
            faculty_details_raw = raw_faculty.find('p')
            details_text = faculty_details_raw.text.strip('\t')
            
            pattern = r"Title:\s*(.*?)\s*Office:\s*(.*?)\s*Phone:\s*(.*?)\s*Email:\s*(.*?)\s*Web:\s*(.*?)(?=\s*Title:|$)"
            match = re.search(pattern, details_text)
            
            if match:
                faculty_data['name'] = name.get_text(strip=True)
                faculty_data['title'] = match.group(1).strip()
                faculty_data['office'] = match.group(2).strip()
                faculty_data['phone'] = match.group(3).strip()
                faculty_data['email'] = match.group(4).strip()
                faculty_data['web'] = match.group(5).strip()
                faculty_list.append(faculty_data)
        
        self.faculty_list = faculty_list
        return faculty_list

    # Q5 Load the faculty data into MongoDB
    def load_faculty(self):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['cpp']
        collection = db['professors']
        for faculty in self.faculty_list:
            if not collection.find_one({'name': faculty['name']}):
                collection.insert_one(faculty)
        
if __name__ == '__main__':
    crawler = FacultyCrawler('https://www.cpp.edu/sci/computer-science/')
    target_url = crawler.crawl_for_target()
    if target_url:
        faculty_list = crawler.crawl_for_faculty()
        crawler.load_faculty()
    else:
        print("Target URL not found.")
        


            

