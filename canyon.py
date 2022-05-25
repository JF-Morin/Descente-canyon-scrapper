# Imports
from dataclasses import dataclass, replace
from requests_html import HTMLSession



# Class: Canyon
@dataclass
class Canyon:
    # Attributes
    country: str = ''
    state: str = ''
    region: str = ''
    city: str = ''
    massif: str = ''
    bassin: str = ''
    water_stream: str = ''
    interets: float = 0.0
    starting_altitude: int = 0
    elevation_drop: int = 0
    length: int = 0
    max_waterfall_height: int = 0
    grade: str = ''
    minimum_rope_length: int = 0
    approach_time: str = ''
    descent_time: str = ''
    exit_time: str = ''
    shuttle_distance: str = ''
    access_description: str = ''
    approach_description: str = ''
    descent_description: str = ''
    exit_description: str = ''
    comments: str = ''

    # Methods

    def fill_canyon_data(self, canyon_url):
        print('\n' + canyon_url)
        session = HTMLSession()
        base_url = 'https://www.descente-canyon.com'
        urls = []
        request = session.get(canyon_url)

        tab = request.html.find('.nav.nav-pills.onglets li')
        if not tab:
            return
        tab_url = base_url + tab[1].find('a')[0].attrs['href']
        description_html = session.get(tab_url)

        # Location description
        location_description = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')
        if not location_description:
            return
        labels = ["Pays","Région","Département","Commune","Massif","Bassin", "Cours d'eau"]
        description_properties = ["country","state","region","city","massif","bassin","water_stream"]
        i = 0
        for index,label in enumerate(labels):
            if label in location_description[1].text:
                setattr(self, description_properties[index], location_description[1].find('span')[i].text)
                i += 1

        # Canyon Interest
        interests = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')[2].search('<strong>{}</strong>')
        self.interets = 0.0 if interests == None else float(interests[0].replace(',','.'))

        # Canyon Starting Altitude
        starting_altitude = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')[3].find('.badge')[0]
        self.starting_altitude = 0 if starting_altitude.text == "??" else int(starting_altitude.text.replace('Alti dép. ','').replace('m',''))

        # Canyon Elevation Drop
        elevation_drop = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')[4].find('.badge')[0]
        self.elevation_drop = 0 if elevation_drop.text == "??" else int(elevation_drop.text.replace('Dénivelé ','').replace('m',''))

        # Canyon Length
        length = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')[5].find('.badge')[0]
        self.length = 0 if length.text == "??" else int(length.text.replace('Longueur ','').replace('m',''))

        # Canyon Max Waterfall Height
        max_waterfall_height = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')[6].find('.badge')[0]
        self.max_waterfall_height = 0 if max_waterfall_height.text == "??" else int(max_waterfall_height.text.replace('Casc. max ','').replace('m',''))

        # Canyon Grade
        grade = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')[7].find('.badge')[0]
        self.grade = "" if grade.text == "??" else grade.text.replace('Cotation ','')

        # Canyon Minimum Rope Length
        minimum_rope_length = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')[8].find('.badge')[0]
        self.minimum_rope_length = 0 if minimum_rope_length.text == "??" else int(minimum_rope_length.text.replace('Corde ','').replace('m','').replace('*',''))

        # Canyon Approach Time
        approach_time = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')[9].find('.badge')[0]
        self.approach_time = "" if approach_time.text == "??" else approach_time.text.replace('Approche: ','')

        # Canyon Descent Time
        descent_time = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')[10].find('.badge')[0]
        self.descent_time = "" if descent_time.text == "??" else descent_time.text.replace('Descente: ','')

        # Canyon Exit Time
        exit_time = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')[11].find('.badge')[0]
        self.exit_time = "" if exit_time.text == "??" else exit_time.text.replace('Retour: ','')

        # Canyon Shuttle Distance
        shuttle_distance = description_html.html.find('.fichetechniqueintegree .list-group .list-group-item')[12].find('.badge')[0]
        self.shuttle_distance = "" if shuttle_distance.text == "??" else shuttle_distance.text.replace('Navette: ','')


        # Text description
        h3_elements = description_html.html.find('.nav.nav-pills.onglets + div')[0].find('h3')
        p_elements = description_html.html.find('.nav.nav-pills.onglets + div')[0].find('p')
        for index,h3 in enumerate(h3_elements):
            if h3.text == 'Accès':
                self.access_description = p_elements[index].text
            elif h3.text == 'Descente':
                self.approach_description = p_elements[index].text
            elif h3.text == 'Retour':
                self.descent_description = p_elements[index].text
            elif h3.text == 'Engagement':
                self.exit_description = p_elements[index].text


        
        # print("Interest: " + str(self.interets) + '/4')
        # print("Sarting elevation: " + str(self.starting_altitude))
        # print("Elevaton drop: " + str(self.elevation_drop))
        # print("Length: " + str(self.length))
        # print("Max Waterfall height: " + str(self.max_waterfall_height))
        # print("Grade: " + self.grade)
        # print("Min Rope Length: " + str(self.minimum_rope_length))
        # print("Approach: " + self.approach_time)
        # print("Descent: " + self.descent_time)
        # print("Exit: " + self.exit_time)
        # print("Shuttle: " + self.shuttle_distance)
        # print('')
   

        return

    

