# Craigslist-Apartment-Scraper

## Install

On Raspberry Pi (Debian Jessie), assuming Python 2.7 & pip are installed:

* `sudo pip install virtualenv`
* Create a virtual environment and activate it
* `sudo apt-get install libssl1.0.0=1.0.1t-1+deb8u6` - Fix to be able to install `libssl-dev`
* `sudo apt-get install python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg62-turbo-dev zlib1g-dev`
* `pip install -r requirements.txt`

## Run

* `cd apt_scraper/`
* `scrapy crawl new_apts`