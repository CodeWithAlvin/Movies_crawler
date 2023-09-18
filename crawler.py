from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests

class Hdhub4u:
    
    def __init__(self):
        self.url = "https://hblinks.pro/page/{page}?s="
        self.movies = {}
        
    def load_url(self, url):
        try:
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html5lib')
        except Exception as e:
            print(f"Error loading {url}: {e}")
            soup = None
        return soup, req.status_code

    def search(self, title):
        self.title = "{title}"
        payload_url = self.url.format(page=1) + title
        pages = []

        soup,status_code = self.load_url(payload_url)

        # checking for no of pages
        if status_code >= 200 and status_code < 300:
        	navigations = soup.find_all('a', attrs = {'class':'page-numbers'})
        	for links in navigations:
        		pages.append(int(links.text)) if links.text.isnumeric() else None

        	self.pages = max(pages)

        	# saving link from first page
        	self.push_movie(soup)

        with ThreadPoolExecutor(max_workers=20) as executor:
            for page in range(2, self.pages+1):
                url = self.url.format(page=page) + title
                executor.submit(self.handle_push, url)
            executor.shutdown()
            
                    
    def push_movie(self, soup):
        try:
            header = soup.find('header', attrs={'class': 'entry-header'})
            heading = header.find('h2', attrs={'class': 'entry-title'})
            text, href = heading.a.text, heading.a.get('href')
            self.movies[text] = href
        except Exception as e:
            print(e)
    
    def handle_push(self,url):
    	soup,status_code = self.load_url(url)
    	if status_code >= 200 and status_code < 300:
    		self.push_movie(soup)
     