
import importlib
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class globalScraper:
    LIMIT_DAYS = 200
    LIMIT_ARTICLES = 20
    def __init__(self, source):
        self.source = source  
        self.data = []

    def run(self):

        module_name = f"controllers.{self.source['name']}.scraper"
        module = importlib.import_module(module_name, package=".")
        main = getattr(module, "main")

        try:
            scraped_data = main(self.LIMIT_DAYS, self.LIMIT_ARTICLES, self.source)
            self.data = scraped_data
            return True
        except:
            return False
        
        

