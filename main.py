# Imports
import sys
from requests_html import HTMLSession
import json
from canyon import Canyon

session = HTMLSession()


def get_country_links():
    urls = []
    base_url = 'https://www.descente-canyon.com'
    request = session.get(base_url + '/canyoning')
    countries = request.html.find('.list-group-item')
    if not countries:
        return []
    for country in countries:
        url = base_url + country.attrs['href']
        urls.append(url)
    return urls

def  get_canyon_list(url):
    base_url = 'https://www.descente-canyon.com'
    canyon_list = []
    # Get Tab URL
    request = session.get(url)
    tab = request.html.find('.nav.nav-pills.onglets li')
    if not tab:
        return []
    tab_url = base_url + tab[1].find('a')[0].attrs['href']
    tab_url_resquest = session.get(tab_url)

    # Get rows data from script tags in HTML
    script = tab_url_resquest.html.find('.clusterize + script')
    if not script:
        return []
    var_rows_str = 'var rows = '
    var_rows_index = script[0].text.index(var_rows_str) + len(var_rows_str) + 1
    searchNom_str = ', searchNom = document.getElementById'
    searchNom_index = script[0].text.index(searchNom_str) - 1
    text_rows_data = script[0].text[var_rows_index:searchNom_index]

    # Get URLs from array
    items = text_rows_data.split(' ,')
    for item in items:
        new_url = base_url + item.split(',')[10]
        canyon_list.append(new_url.replace("'",""))
    return canyon_list

def get_secondary_site_list(url):
    base_url = 'https://www.descente-canyon.com'
    secondary_site_list = []
    # Get Tab URL
    request = session.get(url)
    tab = request.html.find('.nav.nav-pills.onglets li')
    if not tab:
        return []
    tab_url = base_url + tab[2].find('a')[0].attrs['href']
    tab_url_resquest = session.get(tab_url)

    # Get rows data from script tags in HTML
    script = tab_url_resquest.html.find('.clusterize + script')
    if not script:
        return []
    var_rows_str = 'var rows = '
    var_rows_index = script[0].text.index(var_rows_str) + len(var_rows_str) + 1
    searchNom_str = ', searchNom = document.getElementById'
    searchNom_index = script[0].text.index(searchNom_str) - 1
    text_rows_data = script[0].text[var_rows_index:searchNom_index]

    # Get URLs from array
    items = text_rows_data.split(' ,')
    for item in items:
        new_url = base_url + item.split(',')[10]
        secondary_site_list.append(new_url.replace("'",""))
    return secondary_site_list

def main():
    canyons = []
    canyon_urls = []
    country_urls = get_country_links()
    sys.stdout.write('Countries: ' + str(len(country_urls)))
    sys.stdout.write('\n')
    sys.stdout.flush()
    for url in country_urls:
        canyon_urls += get_canyon_list(url)
        canyon_urls += get_secondary_site_list(url)
        sys.stdout.write('\rTotal canyons: ' + str(len(canyon_urls)))
        sys.stdout.flush()
    sys.stdout.write('\n')
    for x in range (4):
        canyon = Canyon()
        canyon.fill_canyon_data(canyon_urls[x])
        canyons += canyon
        sys.stdout.write('\rGet info canyon: ' +str(len(canyons)) + ' of ' + str(len(canyon_urls)))
        sys.stdout.flush()

if __name__ == '__main__':
    main()