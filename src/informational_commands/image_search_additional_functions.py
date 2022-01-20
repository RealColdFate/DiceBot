import requests as rq
from bs4 import BeautifulSoup
from google_images_download import google_images_download


# formats the list into two halves
def format_name_list(name_list: list):
    half_one = name_list[0:len(name_list) // 2]
    half_two = name_list[len(name_list) // 2::]
    out_one = out_two = ''
    for i in range(len(half_one)):
        out_one += f'{i + 1}. {half_one[i]}\n'
    for i in range(len(half_two)):
        out_two += f'{i + len(name_list) // 2 + 1}. {half_two[i]}\n'
    return out_one, out_two


FANTASY_NAME_SOURCE_SITE_URL = 'https://www.fantasynamegen.com/'


def retrieve_names_from_page(search_key):
    url = f"https://www.fantasynamegen.com/{search_key}/short/"
    page_contents = rq.get(url)
    soup = BeautifulSoup(page_contents.text, 'html.parser')

    return soup.find('ul').text.split('\n')[1:-1]


def retrieve_image_urls_of_search_term(search_term, result_limit):
    response = google_images_download.googleimagesdownload()

    arguments = {"keywords": search_term,
                 "limit": result_limit,
                 "no_download": True,
                 "silent_mode": True}
    paths = response.download(arguments)

    images_paths = []
    for k, v in paths[0].items():
        images_paths += v

    return images_paths
