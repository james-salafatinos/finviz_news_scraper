#executed when ran from CLI
try:
    from .utils import scrape, read, get_vocab
except ImportError as e:
    from utils import scrape, read, get_vocab

import argparse

parser = argparse.ArgumentParser(description='finviz scraper')
parser.add_argument('--url', type = str, default = 'https://finviz.com/news.ashx', help = 'Finviz News Site URL')
#Parsed from CLI --> args
args = parser.parse_args()

def main():
    #Gets titles, links, sources, and dates of the current finviz news RSS feed
    scraped_df = scrape(args.url)
    #Gets text from each news article
    df = get_vocab(scraped_df)



if __name__ == "__main__":
    #Ran from CLI
    main()
    
