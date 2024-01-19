from dataclasses import dataclass


@dataclass
class Urls:
    """Class containing all the urls used in the etl process"""

    country_specs = "https://gist.githubusercontent.com/AlexandreGazagnes/57eedb7f88d249f2d5bb85e525e55260/raw/1e559190503cc05f0e298ddddf74934acffb0efe/country_specs.csv"
    crops = "https://gist.githubusercontent.com/AlexandreGazagnes/e47b986ad139b70d03735bd0ebb9e295/raw/c88ff0a9cc114e60b81deb1578389a1599c67a4b/crops.csv"
    production_json = "https://fenixservices.fao.org/faostat/static/bulkdownloads/datasets_E.json"
    production = "https://fenixservices.fao.org/faostat/static/bulkdownloads/Production_Crops_Livestock_E_All_Data_(Normalized).zip"
    population = "https://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv"
    gdp = "https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=csv"
    gbs = "https://gist.githubusercontent.com/AlexandreGazagnes/c57072a70e89f38c4375554f668069ab/raw/32f217d46184c806d3df15687c839c02af7661fd/gbs.csv"
    final = "https://gist.githubusercontent.com/AlexandreGazagnes/c57072a70e89f38c4375554f668069ab/raw/32f217d46184c806d3df15687c839c02af7661fd/gbs.csv"
