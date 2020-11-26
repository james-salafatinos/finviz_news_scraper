# How to create a financial news analysis dataset

## 
1. In your repository folder of your local machine, pull up Git Bash or a terminal.
2. Run `git clone https://github.com/james-salafatinos/finviz_news_scraper.git`
3. Run `cd finviz_news_scraper`
4. Run `py -m venv env` to create a virtual environment
5. Run `env\Scripts\activate` to utilize the new virtual environment
6. With the virtual environment activated, Run `pip install -r requirements.txt` to install packages
7. Run `py setup.py install` to run setup to set up the remainder of the package making it accessible from the command line
8. Run `py finviz_scraper` to execute the program for the current news set on finviz.com

After the program runs, you will find two assets:
1. finviz_news_scraper/data
- Here there will be a .csv file (i.e. "11-26-2020.csv" that contains the link and title data for all the articles pulled
2. finviz_news_scraper/data/obj
- Here you will find a pickled pandas dataframe with all the extracted, trimmed, and cleaned article text.

If you wish to do analysis, open up a jupyter notebook and pull in the pickled dataframe: `df = pd.from_pickle('/data/obj/11-22-2020.pkl')`

