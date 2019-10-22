"""
This file scrapes top 20 lyrics of every reggaeton artist on letras.com.
Input: url slug /mais-acessadas/reggaeton/
Output: lyrics.txt. This file is saved in the input folder for the future lyrics generation (deep learning project)
"""


import requests
import bs4
from bs4 import BeautifulSoup
from pprint import pprint
# import pandas as pd


def scrape(url_slug):     
    LETRAS_ROOT_URL = "https://www.letras.com"
    LETRAS_REGGAETON_URL = LETRAS_ROOT_URL + url_slug

    # OBTENEMOS LA PÁGINA DONDE SALEN TODOS LOS ARTISTAS DE REGGAETON

    response = requests.get(LETRAS_REGGAETON_URL)

    soup = BeautifulSoup(response.text, "html.parser")

    # Acotamos la búsqueda al contenedor
    artists_container = soup.find("ol", {'class': 'top-list_art'})

    # Como ya hemos achicado al contenedor, buscamos el patrón que se repite. En este caso las etiquetas "a"
    artists_html = artists_container.find_all("a")

    # Creamos la lista con las URL de los artistas. Esta lista está compuesta por listas de 2 elementos: URL y nombre del artista.
    artists_href = [[artist.get('href'), artist.text] for artist in artists_html]

    """
    En caso de que quisiéramos guardar artista, título de la canción y la letra en un dataframe:
    df = pd.DataFrame(columns=['Artist', 'Title', 'Lyrics'])
    """

    for artist_href in artists_href:
        artist_href[0] = LETRAS_ROOT_URL + artist_href[0]

        # OBTENEMOS LA PÁGINA DONDE SALEN LOS TÍTULOS DE LAS TOP 20 CANCIONES DEL ARTISTA

        art_response = requests.get(artist_href[0])
        art_soup = BeautifulSoup(art_response.text, "html.parser")

        # Achicamos la búsqueda al contenedor
        songs_container = art_soup.find("ol", {'class': 'cnt-list cnt-list--num cnt-list--col2'})

        # Como ya hemos achicado al contenedor, buscamos el patrón que se repite. En este caso es la etiqueta "a".
        songs_html = songs_container.find_all("a")

        # Creamos la lista con las URL de las canciones. Esta lista está compuesta por listas de 2 elementos: URL y título de la canción.
        songs_href = [[song.get('href'), song.text] for song in songs_html]

        # Imprimimos las URL de cada una de las canciones de los artistas.
        # pprint(songs_href)

        for song_href in songs_href:
            song_href[0] = LETRAS_ROOT_URL + song_href[0]

            # OBTENEMOS LA PÁGINA DONDE SALE LA LETRA DE LA CANCIÓN

            song_response = requests.get(song_href[0])
            song_soup = BeautifulSoup(song_response.text, "html.parser")

            # Achicamos la búsqueda al contenedor
            paragraphs_container = song_soup.find("div", {'class': 'cnt-letra p402_premium'})

            # Como ya hemos achicado al contenedor, buscamos el patrón que se repite. En este caso las etiquetas "p".
            paragraphs_html = paragraphs_container.find_all("p")

            """
            Si quisiéramos sacar las canciones en un dataframe con artista y título, haríamos:
            df = df.append({'Artist': artist_href[1], 'Title': song_href[1], 'Lyrics': paragraphs_html} , ignore_index=True)
            "ignore_index=True" para que los index se vayan añadiendo de forma incremental.
            """
            paragraph = "".join(str(paragraphs_html))
            with open("lyrics.txt", 'a') as file:
                try:
                    file.write(paragraph[1:-1])
                except Exception as e: print(e)
            file.close()
            

def main():
    url_slug = "/mais-acessadas/reggaeton/" # where complete URL is https://www.letras.com/<url_slug>
    scrape(url_slug)

if __name__ == "__main__":
    main()