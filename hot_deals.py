import requests
from bs4 import BeautifulSoup
from typing import List
from fastapi import FastAPI

class Item:
    def __init__(self, title: str, votes: int, replies: int):
        self.title = title
        self.votes = votes
        self.replies = replies

def scrape_data() -> List[Item]:
    url = "https://forums.redflagdeals.com/hot-deals-f9/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    list_threads = soup.find('ul', {'class': 'list_threads'})
    thread_titles = list_threads.find_all('a', {'class': 'thread_title'})
    vote_counts = list_threads.find_all('span', {'class': 'thread_vote_count'})
    reply_counts = list_threads.find_all('span', {'class': 'thread_reply_count'})

    items = []
    for i in range(len(thread_titles)):
        title = thread_titles[i].text.strip()
        votes = int(vote_counts[i].text.strip())
        replies = int(reply_counts[i].text.strip().split()[0])
        items.append(Item(title, votes, replies))

    return items

app = FastAPI()

items = scrape_data()

@app.get("/hot_deals")
async def get_items():
    global items
    items = scrape_data()
    return items
