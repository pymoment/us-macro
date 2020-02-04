import os
import re
from bs4 import BeautifulSoup


def parse_html(url, html):
    '''
    A simple script to create tipue content by searching for documentation
    files under given folders.

    Copyright (C) 2016 Bo Peng (bpeng@mdanderson.org) under GNU General Public License
    '''
    with open(html, 'rb') as content:
        soup = BeautifulSoup(content, "html.parser", from_encoding='utf-8')
        #
        # try to get the title of the page from h1, h2, or title, and
        # uses filename if none of them exists.
        #
        title = soup.find('h1')
        if title is None:
            title = soup.find('h2')
        if title is None:
            title = soup.find('title')
        if title is None:
            title = os.path.basename(html).rsplit('.')[0]
        else:
            title = title.get_text()
        maintitle = soup.find('h1')
        if maintitle is None:
            maintitle = soup.find('h2')
        if maintitle is None:
            maintitle = soup.find('title')
        if maintitle is None:
            maintitle = os.path.basename(html).rsplit('.')[0]
        else:
            maintitle = maintitle.get_text()

        # remove special characters which might mess up js file
        title = re.sub(r'[{}^a-zA-Z0-9_\.\-]'.format(chr(182)), ' ', title)
        #
        # sear
        all_text = []
        for header in soup.find_all(re.compile('^h[1-6]$')):
            # remove special character
            part = re.sub(r'[^a-zA-Z0-9_\-=\'".,\\]',
                          ' ',
                          header.get_text()).replace('"', "'").strip() + "\n"
            part = re.sub(r'\s+', ' ', part)
            ids = [x for x in header.findAll('a') if x.get('id')]
            if ids:
                tag = '#' + ids[0].get('id')
            else:
                hrefs = header.findAll('a', {'class': 'anchor-link'})
                if hrefs:
                    tag = hrefs[0].get('href')
                else:
                    tag = ''
            part = '{{"mainTitle": "{}", "title": "{}", "text": "{}", "tags": "", "mainUrl": "{}", "url": "{}"}}'.format(
                    re.sub(chr(182), '', maintitle), re.sub(chr(182), '', header.get_text()), part, url, url + tag)
            all_text.append(part)
    return all_text


def generate_tipue_content(html_files, base_url, docs_dir):
    """ input is a list of html files and their url """
    n = len(docs_dir)
    text = [parse_html(url, html)
            for (url, html) in [(os.path.join(base_url, item[n:]), item)
                                for item in html_files]]
    # write the output to file.
    with open(os.path.join(docs_dir,
                           'site_libs/tipuesearch',
                           'tipuesearch_content.js'), 'w') as out:
        out.write('''\
var tipuesearch = {{"pages": [
{}
]}};
'''.format(',\n'.join(sum(text, []))))
