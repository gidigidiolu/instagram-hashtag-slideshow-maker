# Instagram HashTag SlideShow

This program uses Instagram Crawler (<https://github.com/huaying/instagram-crawler)> to crawl Instagram hashtags and create a slideshow (html file).

This crawler may fail due to updates on instagram’s website. Please contact me if you encounter any problems.

## Install

1. Make sure you have Chrome browser installed.
2. Download [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) and put it into bin folder: `./inscrawler/bin/chromedriver`
3. Install Selenium: `pip install -r requirements.txt`
4. `cp inscrawler/secret.py.dist inscrawler/secret.py`

## Usage

### Example

To create a slideshow with 1000 images of #totliv. App restarts every 24 hours from first crawl unless stopped.

```shell
python hashtag.py totliv 1000
```

To create a slideshow with 1000 images of #totliv. App restarts every 360 seconds from first crawl unless stopped.

```shell
python hashtag.py totliv 1000 360
```

To explicitly supply an input html file.

```shell
python hashtag.py totliv 1000 --html slideshow.html

python hashtag.py totliv 1000 360 --html sideshow.html
```

To add a '--clear' flag.

```shell
python hashtag.py totliv 1000 --clear

python hashtag.py totliv 1000 360 --clear

python hashtag.py totliv 1000 --html slideshow.html --clear

python hashtag.py totliv 1000 360 --html sideshow.html --clear
```