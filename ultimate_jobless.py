from bs4 import BeautifulSoup
import requests


url = 'https://cc.dinus.ac.id/lowongan/daftar'
request_page = requests.get(url, verify=False)
if request_page.status_code != 200:
    print("request error")
    quit()

the_html = request_page.text
soup = BeautifulSoup(the_html, 'html.parser')
# print(soup.prettify())

aj = {}

for available_job in soup.find_all('div', {'class': 'col-lg-3 col-md-6 col-12 mb-3'}):

    job_type = available_job.find('h4', {'class': 'card-title mt-2'}).text
    company = ' '.join(str(available_job.find('h5', {'class': 'card-subtitle mb-2 text-muted'}).text).split())
    url = ' '.join(str(available_job.find('a', {'class': 'mt-3 btn btn-sm btn-info'})['href']).split())
    line = ' '.join(str(available_job.find('p', {'class': 'card-text'}).text).split())
    text = line.split('|')
    min_requirement = text[0]
    deadline = text[1][text[1].lower().find('deadline') + len("deadline: "):]
    cities = ' '.join(text[1][:text[1].lower().find('deadline')].split())

    if company not in aj:
        aj[company] = [
            {'type            ': job_type,
             'min requirement ': min_requirement,
             'cities          ': cities,
             'deadline        ': deadline,
             'url             ': url
             }
        ]
    else:
        aj[company].append(
            {'type            ': job_type,
             'min requirement ': min_requirement,
             'cities          ': cities,
             'deadline        ': deadline,
             'url             ': url
             }
        )

i = 0
for company, job_list in aj.items():
    i += 1
    print(f'[{i}]=======================================================')
    print(f'    company : {company}')
    u = 0
    for job in job_list:
        u += 1
        print(f'    [{u}]---')
        for key, value in job.items():
            print(f'        {key} : {value}')
        print("")
    print("")
