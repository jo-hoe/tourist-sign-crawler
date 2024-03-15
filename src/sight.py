
import csv


class Sight():

    def __init__(self):
        self._signs_on_kilometer_on_highway = []
        self._wiki_link = None

    @property
    def name(self) -> str:
        return self._name
    
    def set_name(self, value : str):
        self._name = value
    
    @property
    def signs_on_kilometer_on_highway(self) -> list[float]:
        return self._signs_on_kilometer_on_highway
    
    def add_kilometer(self, value : float):
        self._signs_on_kilometer_on_highway.append(value)
    
    @property
    def highway(self) -> str:
        return self._highway
    
    def set_highway(self, value : str):
        self._highway = value
    
    @property
    def wiki_link(self) -> str:
        return self._wiki_link
    
    def set_wiki_link(self, value : str):
        self._wiki_link = value
    
    @property
    def location(self) -> tuple[float, float]:
        return self._location
    
    def set_location(self, value : tuple[float, float]):
        self._location = value
    
def export_sights_to_csv(sights : list[Sight], filename : str) -> None:
    fields = ['name', 'signs_on_kilometer_on_highway', 'highway', 'wiki_link', 'location']
    
    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        
        writer.writeheader()
        for sight in sights:
            writer.writerow({
                'name': sight.name,
                'signs_on_kilometer_on_highway': sight.signs_on_kilometer_on_highway,
                'highway': sight.highway,
                'wiki_link': sight.wiki_link,
                'location': sight.location
            })