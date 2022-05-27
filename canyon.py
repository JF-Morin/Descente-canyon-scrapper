# Imports
from dataclasses import dataclass, replace
import requests_html

# Class: Canyon
@dataclass
class Canyon:
    def __init__(self):
        # Attributes
        self.name: str = ''
        self.country: str = ''
        self.state: str = ''
        self.region: str = ''
        self.city: str = ''
        self.massif: str = ''
        self.bassin: str = ''
        self.water_stream: str = ''
        self.interest: float = 0.0
        self.starting_altitude: int = 0
        self.elevation_drop: int = 0
        self.length: int = 0
        self.max_waterfall_height: int = 0
        self.grade: str = ''
        self.minimum_rope_length: int = 0
        self.approach_time: str = ''
        self.descent_time: str = ''
        self.exit_time: str = ''
        self.shuttle_distance: str = ''
        self.access_description: str = ''
        self.approach_description: str = ''
        self.descent_description: str = ''
        self.exit_description: str = ''
        self.comments: str = ''
    
    def __iter__(self):
        return self

    # Methods

    def parse_html_canyon_data(self, response):
        description_html = response.html
        # Canyon name
        self.name = description_html.find('.col-md-9')[0].find('h1')[0].search('<strong>{}</strong>')[0]

        # Location description
        location_description = description_html.find('.fichetechniqueintegree .list-group .list-group-item')

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
        interest = description_html.find('.fichetechniqueintegree .list-group .list-group-item')[2].search('<strong>{}</strong>')
        self.interest = 0.0 if interest == None else float(interest[0].replace(',','.'))

        # Canyon Starting Altitude
        starting_altitude = description_html.find('.fichetechniqueintegree .list-group .list-group-item')[3].find('.badge')[0]
        self.starting_altitude = 0 if starting_altitude.text == "??" else int(starting_altitude.text.replace('Alti dép. ','').replace('m',''))

        # Canyon Elevation Drop
        elevation_drop = description_html.find('.fichetechniqueintegree .list-group .list-group-item')[4].find('.badge')[0]
        self.elevation_drop = 0 if elevation_drop.text == "??" else int(elevation_drop.text.replace('Dénivelé ','').replace('m',''))

        # Canyon Length
        length = description_html.find('.fichetechniqueintegree .list-group .list-group-item')[5].find('.badge')[0]
        self.length = 0 if length.text == "??" else int(length.text.replace('Longueur ','').replace('m',''))

        # Canyon Max Waterfall Height
        max_waterfall_height = description_html.find('.fichetechniqueintegree .list-group .list-group-item')[6].find('.badge')[0]
        self.max_waterfall_height = 0 if max_waterfall_height.text == "??" else int(max_waterfall_height.text.replace('Casc. max ','').replace('m',''))

        # Canyon Grade
        grade = description_html.find('.fichetechniqueintegree .list-group .list-group-item')[7].find('.badge')[0]
        self.grade = "" if grade.text == "??" else grade.text.replace('Cotation ','')

        # Canyon Minimum Rope Length
        minimum_rope_length = description_html.find('.fichetechniqueintegree .list-group .list-group-item')[8].find('.badge')[0]
        self.minimum_rope_length = 0 if minimum_rope_length.text == "??" else int(minimum_rope_length.text.replace('Corde ','').replace('m','').replace('*',''))

        # Canyon Approach Time
        approach_time = description_html.find('.fichetechniqueintegree .list-group .list-group-item')[9].find('.badge')[0]
        self.approach_time = "" if approach_time.text == "??" else approach_time.text.replace('Approche: ','')

        # Canyon Descent Time
        descent_time = description_html.find('.fichetechniqueintegree .list-group .list-group-item')[10].find('.badge')[0]
        self.descent_time = "" if descent_time.text == "??" else descent_time.text.replace('Descente: ','')

        # Canyon Exit Time
        exit_time = description_html.find('.fichetechniqueintegree .list-group .list-group-item')[11].find('.badge')[0]
        self.exit_time = "" if exit_time.text == "??" else exit_time.text.replace('Retour: ','')

        # Canyon Shuttle Distance
        shuttle_distance = description_html.find('.fichetechniqueintegree .list-group .list-group-item')[12].find('.badge')[0]
        self.shuttle_distance = "" if shuttle_distance.text == "??" else shuttle_distance.text.replace('Navette: ','')


        # Text description
        h3_elements = description_html.find('.nav.nav-pills.onglets + div')[0].find('h3')
        p_elements = description_html.find('.nav.nav-pills.onglets + div')[0].find('p')
        for index,h3 in enumerate(h3_elements):
            if h3.text == 'Accès':
                self.access_description = p_elements[index].text
            elif h3.text == 'Descente':
                self.approach_description = p_elements[index].text
            elif h3.text == 'Retour':
                self.descent_description = p_elements[index].text
            elif h3.text == 'Engagement':
                self.exit_description = p_elements[index].text
        
        return

    

