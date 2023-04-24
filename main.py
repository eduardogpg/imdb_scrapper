import requests
from bs4 import BeautifulSoup 

IMDB_FILE = 'imdb.txt'

def generate_request(url: str = 'http://www.imdb.com/trailers/') -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text

    return None


def read_imdb_file() -> str:
    try:
        with open(IMDB_FILE) as file:
            return file.read()
    
    except Exception as err:
        return None


def imdb_content(url: str = 'http://www.imdb.com/trailers/') -> str:
    content = read_imdb_file()
    if not content:
        content = generate_request()

        with open(IMDB_FILE, 'w') as file:
            file.write(content)

    return content


def movie(div):
    div_childre = div.findChildren("div" , recursive=False)
    
    div_with_more_information = children[0].findChildren('div', recursive=False)
    print(div)


    trailer_type = children[1].text # Div
    date = children[2].span.text

    print(trailer_type)
    print(date)



def main():
    content = imdb_content()

    if not content:
        return False

    soup = BeautifulSoup(content, 'html.parser')
    div = soup.find('div', {
        'class': 'ipc-sub-grid ipc-sub-grid--page-span-3 ipc-sub-grid--wrap sc-1f3a3cbd-0 iorTDA',
    })  
    
    divs = div.find_all("div", recursive=False)
    movie(divs[0])





if __name__ == '__main__':
    main()