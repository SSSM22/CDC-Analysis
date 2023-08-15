import requests
from bs4 import BeautifulSoup

def leetrate(leetu):
    url = f"https://leetcode.com/{leetu}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rank_element = soup.find(
            class_="text-[24px] font-medium text-label-1 dark:text-dark-label-1")
        if rank_element:
            rank = rank_element.get_text().strip()
            print(rank)
        else:
            return "Ranking not found."
    else:
        return "Unable to connect to LeetCode."



id="saishivamani_s"    
leetrate(id)    