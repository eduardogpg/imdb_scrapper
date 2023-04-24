import csv
import requests
from bs4 import BeautifulSoup 
from collections import namedtuple


URL = 'https://www.imdb.com/calendar/?region=MX&type=MOVIE'
IMDB_FILE = 'imdb.txt'

def generate_request() -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        return response.text

    return None


def read_imdb_file() -> str:
    try:
        with open(IMDB_FILE) as file:
            return file.read()
    
    except Exception as err:
        return None


def imdb_content() -> str:
    content = read_imdb_file()
    if not content:
        content = generate_request()

        with open(IMDB_FILE, 'w') as file:
            file.write(content)
    
    return content


def generate_string_points(tag_list):
    return ','.join([ li.span.text for li in tag_list.find_all('li') ])


def generate_movie(li_tag) -> None:
    div_tag = li_tag.find('div', 
        {'class': 'ipc-metadata-list-summary-item__c'}
    )

    name = div_tag.div.a.text
    details = div_tag.find_all('ul')

    categories = generate_string_points(details[0])
    actors = generate_string_points(details[1]) if len(details) == 2 else 'None'
    
    movie = namedtuple('Movie', ['name', 'categories', 'actors'])
    return movie(name, categories, actors)
   

def main():
    content = imdb_content()

    if not content:
        return False

    soup = BeautifulSoup(content, 'html.parser')
    li_tags = soup.findAll('li', {
        'data-testid': 'coming-soon-entry',
        'class': 'ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-8c2b7f1f-0 bpqYIE'
    })

    movies = [ generate_movie(movie) for movie in li_tags]
    generate_csv(movies)


def generate_csv(movies):

    with open('movies.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow( ['name', 'categories', 'actors']) 

        for movie in movies:
            writer.writerow(movie)


if __name__ == '__main__':
    main()