import datetime
import os
import time

import click
import progressbar
from bs4 import BeautifulSoup

from crawler import get_posts_by_hashtag


def __init__html():
    """Intialise an HTML Document
    
    Returns:
        str -- string representation of a HTML Document
    """
    return ('<!DOCTYPE html>\n\n<html>\n<head>\n<title>SlideShow</title>\n'
            '<link crossorigin="anonymous" '
            'href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/'
            'bootstrap.min.css" '
            'integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iu'
            'XoPkFOJwJ8ERdknLPMO" '
            'rel="stylesheet"/>\n<link crossorigin="anonymous" '
            'href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" '
            'integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRy'
            'MA2Fd33n5dQ8lWUE00s/" '
            'rel="stylesheet"/>\n<style>\n      body {\n      '
            'background-color: #000000;\n      margin-top: 10px;\n      }\n   '
            '   .mySlides {display: none}\n      .col {\n        '
            'height:100vh;\n      }\n\n      img{\n        max-width: 100%;\n'
            '        object-fit: cover;\n        height: calc(100vh - 35px);\n'
            '      }\n      .item:last-child {\n        max-height:35px; '
            '/* set here your last-item height */\n      }\n      '
            '/* Caption text */\n      .text {\n      color: #ffffff;\n      '
            'font-size: 15px;\n      padding: 8px 12px;\n      '
            'position: absolute;\n      bottom: 8px;\n      width: 100%;\n    '
            '  text-align: center;\n      }\n      /* Fading animation */\n   '
            '   .fade {\n      -webkit-animation-name: fade;\n     '
            ' -webkit-animation-duration: 7s;\n      animation-name: fade;\n '
            '     animation-duration: 7s;\n      }\n      @-webkit-keyframes '
            'fade {\n      from {opacity: .7} \n      to {opacity: 1}\n    '
            '  }\n      @keyframes fade {\n      from {opacity: .7} \n     '
            ' to {opacity: 1}\n      }\n    </style>\n</head>\n<body>\n<div '
            'class="container"></div>\n<br/>\n<script>\n    '
            '  var slideIndex = 0;\n      showSlides();\n      \n     '
            ' function showSlides() {\n        var i;\n       '
            ' var slides = document.getElementsByClassName("mySlides");\n     '
            '   for (i = 0; i < slides.length; i++) {\n         '
            ' slides[i].style.display = "none"; \n        }\n      '
            '  slideIndex++;\n        if (slideIndex > slides.length) '
            '{slideIndex = 1} \n       '
            ' slides[slideIndex-1].style.display = "block"; \n       '
            ' setTimeout(showSlides, 7000); // Change image every 7 seconds\n'
            '      }\n    </script>\n</body>\n</html>')


def __create_content(img_src, alt):
    """Page Element for an image
    
    Arguments:
        img_src {str} -- image source
        alt {str} -- alternative text for image
    """
    return('<div class="mySlides fade">\n'
           '<div class="col d-flex justify-content-center">\n'
           '<div class="d-flex flex-column">\n<div class="item">'
           f'<img alt={alt} class="rounded" src="{img_src}"/>'
           '</div>\n</div>\n</div>\n</div>')


def create_slideshow(soup=None, hashtags=None, html_file='index.html'):
    """Creates hashtag slideshow as an HTML Document
    
    Keyword Arguments:
        soup {BeautifulSoap} -- A data structure representing a parsed HTML
        document (default: {None})
        hashtags {list} -- a list of hashtag urls and their respective keys
        (default: {None})
        html_file {str} -- an HTML file (default: {'index.html'})
    
    Returns:
        BeautifulSoap -- A data structure representing a parsed HTML document
    """
    target = soup.find(class_= 'container')

    bar = progressbar.ProgressBar(max_value=len(hashtags),
                                  prefix='Updating HTML file: ')
    bar.start()
    for hashtag in hashtags:
        img_src = hashtag['img_url']
        img_key = hashtag['key']
        # url_alt = img_src.split('?')[0]
        
        # skip inserting URL if it already exists in target
        search_result = target.find(attrs={'alt': img_key})
        if search_result is None:
            content = __create_content(img_src, alt=img_key)

            # create a temporary document from your HTML
            temp = BeautifulSoup(content, "html.parser")

            # the nodes we want to insert are children of the <body> in `temp`
            nodes_to_insert = temp.children

            # insert them, in source order
            for j, node in enumerate(nodes_to_insert):
                target.insert(j, node)

        bar += 1
    bar.finish()
    return soup


def write_soup_to_file(output_file="index.html", soup=None):
    with open(output_file, "w", encoding='utf-8') as file:
        file.write(str(soup))

@click.command()
@click.argument('hashtag')
@click.argument('number', default=100)
@click.argument('sleep_time', default=86400)
@click.option('--clear', is_flag=True)
@click.option('--html', default='index.html', help='html file to update',
              type=click.Path())
def main(hashtag, number, sleep_time, clear, html):
    soup = None

    if os.path.exists(html):
        # open file and check if the slideshow is for the current hashtag
        with open(html, encoding='utf8') as fp:
            soup = BeautifulSoup(fp, "html.parser")

        tag = soup.title.string.split(' ')[0]
        if tag != f'#{hashtag}' and not clear:
            raise click.ClickException(f"{html} is for a different hashtag. "
                                       "Please include the --clear flag to "
                                       "remove file.")
        if clear:
            os.remove(html)

    if not os.path.exists(html):
        soup = BeautifulSoup(__init__html(), "html.parser")

    while True:
        print('>> App Stated - Please be patient.. '
              'This may take sometime to complete...')

        current_time = datetime.datetime.now()
        if os.path.exists(html):
            # get updated soup
            with open(html, encoding='utf8') as fp:
                soup = BeautifulSoup(fp, "html.parser")

        hashtags = get_posts_by_hashtag(tag=hashtag, number=number)
        soup = create_slideshow(soup=soup, hashtags=hashtags)

        # update html's title
        title = soup.title.string
        update_title = f'#{hashtag} slideshow'
        if title != update_title:
            soup.title.string = update_title
 
        write_soup_to_file(output_file=html, soup=soup)
        print(f'>> {html} has been updated.')

        # sleep_time in seconds
        next_time = current_time + datetime.timedelta(seconds=sleep_time)
        print(f'>> App will wake in {next_time}')
        
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
