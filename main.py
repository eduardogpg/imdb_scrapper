import csv
import requests
from bs4 import BeautifulSoup

URL = 'https://www.imdb.com/calendar/?region=MX'

"""
1.- Obtener el maqueto HTML
    - Si el archivo HTML no existe de forma local, crearlo.
    - Si el archivo HTML existe de forma local, obtener su contenido.
2.- Obtener la información
    - Nombre
    - Categorias
    - Reparto
3.- Generar un archivo CSV
"""

def get_imdb_content():
    """Get the content of the IMDB calendar page

    Returns:
        string -- The content of the IMDB calendar page
        None -- If the request was not successful
    """
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(URL, headers=headers) # 20x - 30x - 40x - 50x
    if response.status_code == 200:
        return response.text
    
    return None
    

def create_imdb_file_local(content):
    """Crear un archivo local a partir del maquetado de un sitio web."""
    try:
        with open('imdb.html', 'w') as file:
            file.write(content)
    except:
        pass


def get_imdb_file_local():
    """Lee el contenitdo de un archivo local"""
    content = None
    
    try:
        with open('imdb.html', 'r') as file:
            content = file.read()
    except:
        pass
    
    return content


def get_local_imdb_content():
    """Obtiene el contenido del maquetado de Imdb. Ya sea de forma local o del servidor"""
    content = get_imdb_file_local()
    
    if content:
        return content

    content = get_imdb_content()
    create_imdb_file_local(content)

    return content
    


def create_movie(tag):
    main_div = tag.find('div', {'class': 'ipc-metadata-list-summary-item__c' })
        
    name =  main_div.div.a.text
    ul_categories = main_div.find('ul', {
        'class': 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base'
    })

    ul_cast = main_div.find('ul', {
        'class': 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base'
    }) # None

    cast = None
    categories = [ category.span.text for category in  ul_categories.find_all('li') ]
    
    cast = [ cast.span.text for cast in ul_cast.find_all('li') ] if ul_cast else []
    
    return (name, categories, cast) # Retornamos un tupla



def main():
    content = get_local_imdb_content()
    
    # HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    li_tags = soup.find_all('li', {
        'data-testid': 'coming-soon-entry',
        'class': 'ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-8c2b7f1f-0 bpqYIE'
    })

    movies = []
    for tag in li_tags:
        movie = create_movie(tag)
        movies.append(movie)

    with open('movies.csv', 'w') as file:
        writer = csv.writer(file, delimiter="-")
        writer.writerow(['name', 'categories', 'cast'])

        for movie in movies:
            writer.writerow([
                movie[0], # name
                ",".join(movie[1]), # categories
                ",".join(movie[2]), # cast
            ])



if __name__ == '__main__':
    main()
