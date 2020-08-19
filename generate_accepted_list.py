from bs4 import BeautifulSoup
import requests

import constants

handle = constants.HANDLE
base_url = f'https://codeforces.com/submissions/{handle}/'

source = requests.get(base_url).text

soup = BeautifulSoup(source, 'lxml')

pages = []
for span in soup.find_all('span', class_='page-index'):
    pages.append(int(span.a.text))

max_page = max(pages)
for page in range(1, max_page + 1):
    if page not in pages:
        pages.append(page)
pages.sort(reverse=True)

base_url += 'page/'
accepted = []
for page in pages:
    cur_url = base_url
    cur_url += f'{page}'
    
    source = requests.get(cur_url).text
    soup = BeautifulSoup(source, 'lxml')

    for submission in soup.find_all('span', class_='submissionVerdictWrapper'):
        verdict = submission['submissionverdict']
        if verdict == 'OK':
            accepted.append(submission['submissionid'])

with open('accepted_list.txt', 'w') as f:
    f.write('ac_submissions_id')
    for ac in accepted:
        f.write(ac + '\n')
