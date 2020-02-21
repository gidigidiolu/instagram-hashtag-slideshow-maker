import datetime
import time

import click
import progressbar
from bs4 import BeautifulSoup

from crawler import get_posts_by_hashtag


def __create_content(img_url):
    return ('<div class="mySlides fade">'
            '<div class="col d-flex justify-content-center">'
            '<div class="d-flex flex-column">'
            '<div class="item">'
            f'<img class="rounded" src="{img_url}">'
            '</div>'
            '</div>'
            '</div>'
            '</div>')


def create_slideshow(html_file='index.html', clear_target=False,
                     hashtags=None):
    with open(html_file, encoding='utf8') as fp:
        soup = BeautifulSoup(fp, "html.parser")

    target = soup.find(class_= 'container')

    if clear_target:
        target.clear()

    bar = progressbar.ProgressBar(max_value=len(hashtags),
                                  prefix='Updating HTML file: ')
    bar.start()
    for hashtag in hashtags:
        img_url = hashtag['img_url']
        
        # skip inserting URL if it already exists in target
        search_result = target.find(attrs={'src': img_url})
        if search_result is None:
            content = __create_content(img_url)

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
              type=click.Path(exists=True))
def main(hashtag, number, sleep_time, clear, html):
    while True:
        print('>> App Stated - Please be patient.. '
              'This may take sometime to complete...')

        current_time = datetime.datetime.now()

        # set clear if hashtag is different
        with open(html, encoding='utf8') as fp:
            soup = BeautifulSoup(fp, "html.parser")

        tag = soup.title.string.split(' ')[0]
        if tag != f'#{hashtag}' and not clear:
            raise click.ClickException(f"{html} contains a different hashtag. "
                                       "Please include the --clear flag to "
                                       "clear images.")

        hashtags = get_posts_by_hashtag(tag=hashtag, number=number)
        if clear:
            soup = create_slideshow(html_file=html, hashtags=hashtags,
                                    clear_target=True)
        else:
            soup = create_slideshow(html_file=html, hashtags=hashtags)

        # update html's title
        soup.title.string = f'#{hashtag} SlideShow'
        write_soup_to_file(soup=soup)
        print(f'>> {html} has been updated.')

        # sleep_time in seconds
        next_time = current_time + datetime.timedelta(seconds=sleep_time)
        print(f'>> App will wake in {next_time}')
        
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
