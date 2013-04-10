#!/usr/bin/env python2
import os
import lxml.html

DIR = os.path.join('downloads', 'datasets')

def main():
    pages = filter(lambda page: '.html' == page[-5:], os.listdir(DIR))
    viewids = set()
    for page in pages:
        html = lxml.html.parse(os.path.join(DIR, page))
        viewids = viewids.union(parse(html))
    print ' '.join(viewids)

def parse(html):
    'Get the viewids out.'
    return set(map(unicode, html.xpath('//tr[@itemtype="http://schema.org/Dataset"]/@data-viewid')))

if __name__ == '__main__':
    main()
