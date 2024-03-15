
from concurrent.futures import ThreadPoolExecutor
from src import sight_crawler
from src.openstreetmap import get_coordinates
from src.sight import export_sights_to_csv
from src.wiki_location_crawler import get_location_from_wiki


def set_location_for_item(item):
    if item.wiki_link is not None:
        location = get_location_from_wiki(item.wiki_link)
        if location is not None:
            item.set_location(location)
            return
        
    location = get_coordinates(item.name.replace("Historischer Stadtkern", "").strip())
    item.set_location(location)

if __name__ == "__main__": 
    items = sight_crawler.get_sights()

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(set_location_for_item, items)
    
    export_sights_to_csv(items, "unterrichtungstafeln.csv")