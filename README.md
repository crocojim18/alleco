# `alleco`
### Tracking the governments of Allegheny County's 130 municipalities

<img alt="A map of Allegheny County with completed municipalities highlighted." src="/alleco/supp_data/map.svg" height="500">

_Key: Green means the municipality's spider is working, red means otherwise_

## What is this?
This is a project to understand and keep track of the governments of the 130 municipalities in Allegheny County, Pennsylvania. Because there is no (known) centralized database nor predictable structure to how those governments are organized or who runs them, we have to do things the most efficient way I can figure: webscraping each municipality's website.

## What does this use?
`alleco` uses the open-source scraping framework [Scrapy](https://scrapy.org/) and is written in Python 3. Currently I do not believe there are any other dependencies but it is likely we will use other things to do further NLP on this data in the future.

## How does one use this?
There are a couple of ways you can use this.
1. You can use the data in `results` to see what offices we have scraped and from where we scraped them
1. You can compare it to the data from the [Allegheny County elections site](https://www.alleghenycounty.us/elections/election-results.aspx).
1. You can write new spiders! There are a lot of these municipalities to scrape.

## How is this structured?
This repository is structured as such:
* `alleco`: This is the bulk of the project
  * There are many Scrapy-related files in here but notably ``spiders`` holds all of the spiders in the project, one for every municipal body. The naming convention for spiders is `municipality_name_*` where `*` is `b` if it is a borough, `t` if it is a township, and `c` if it is a city.
* `results`: This folder holds the scraped data, in CSV format, with each file named after the municipality spider.
* `Allegheny_Municipalities.xlsx`: An Excel file listing the municipalities and showcasing some of the manual work I did prior to deciding to webscrape the data.
* `getER.py`: This searches the `contest name` column of the municipal election records from 2017 and 2019 (found in `alleco/supp_data`) for the arguments of the script. It is used to find what offices exist for a given municipality. It is possible that some extant offices are not listed (2015 didn't come in CSV format and it's possible a 6-year term position would be missed) or extinct offices are listed (if the position was abolished after 2017/2019). Generally it is extremely helpful though.
  * Usage: `python getER.py bethel park` for [Bethel Park](https://en.wikipedia.org/wiki/Bethel_Park,_Pennsylvania). Note: this will not account for abbreviations (e.g. [Mt. Oliver vs. Mount Oliver](https://en.wikipedia.org/wiki/Mount_Oliver,_Pennsylvania)), but it works using regex so that can be used as well
* `run.py`: A program that runs all of the spiders and compares them with the previously scraped data to see if there are any of the changes/see if the websites have broken.
  * Usage: `python run.py`

## License
[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)
