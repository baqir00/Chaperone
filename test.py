import requests
from bs4 import BeautifulSoup

user = 'babe'
url = 'https://www.hackerearth.com/users/pagelets/babe/coding-data/'.format(user)
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
problems_solved = soup.find(string='Problems Solved').find_next().text

print(problems_solved)