# Imports
import sys
from requests_html import HTMLSession
import csv
import time

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

def get_canyon_list(url):
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

def get_canyon_tab_url(url):
    base_url = 'https://www.descente-canyon.com'
    request = session.get(url)
    tab = request.html.find('.nav.nav-pills.onglets li')
    if not tab:
        return ''
    tab_url = base_url + tab[1].find('a')[0].attrs['href']
    # description_html = session.get(tab_url)
    return tab_url

def main():
    canyons = []
    canyon_urls = []
    country_urls = get_country_links()
    sys.stdout.write('Countries: ' + str(len(country_urls)))
    sys.stdout.write('\n')
    sys.stdout.flush()

    # Get canyon urls
    for url in country_urls:
        canyon_urls += get_canyon_list(url)
        canyon_urls += get_secondary_site_list(url)
        sys.stdout.write('\rTotal canyons: ' + str(len(canyon_urls)))
        sys.stdout.flush()
    sys.stdout.write('\n')

    # Get canyons data
    for canyon_url in canyon_urls:
        canyon = Canyon()
        response = ''
        time_to_wait = 5
        resp_count = 0
        while response == '':
            try:
                if resp_count >=100:
                    time.sleep(time_to_wait)
                    resp_count = 0
                tab_url = get_canyon_tab_url(canyon_url)
                response = session.get(tab_url)
                break
            except:
                print("Connection refused by the server: sleep for " + str(time_to_wait) + " seconds")
                # session.close()
                # session = None
                # session = HTMLSession()
                time.sleep(time_to_wait)
                time_to_wait += 5
                continue

        # tab_url = get_canyon_tab_url(canyon_url)
        # response = session.get(tab_url)
        
        canyon.parse_html_canyon_data(response)
        canyons.append(canyon)
        sys.stdout.write('\rGet info canyon: ' +str(len(canyons)) + ' of ' + str(len(canyon_urls)))
        sys.stdout.flush()
    
    # Save canyons to CSV file
    headers = ['Name','Country','State','Region','City','Massif','Bassin','Water Stream','Interest','Starting Altitude','Elevation Drop','Length','Max Waterfall Height','Grade','Minimum Rope Length','Approach Time','Descent Time','Exit Time','Shuttle Distance','Access Description','Approach Description','Descent Description','Exit Description']
    with open('Canyons_DB.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(headers)

        # write the data
        for canyon in canyons:
            data = [canyon.name,
                    canyon.country,
                    canyon.state,
                    canyon.region,
                    canyon.city,
                    canyon.massif,
                    canyon.bassin,
                    canyon.water_stream,
                    canyon.interest,
                    canyon.starting_altitude,
                    canyon.elevation_drop,
                    canyon.length,
                    canyon.max_waterfall_height,
                    canyon.grade,
                    canyon.minimum_rope_length,
                    canyon.approach_time,
                    canyon.descent_time,
                    canyon.exit_time,
                    canyon.shuttle_distance,
                    canyon.access_description,
                    canyon.approach_description,
                    canyon.descent_description,
                    canyon.exit_description]
            writer.writerow(data)

    

if __name__ == '__main__':
    main()