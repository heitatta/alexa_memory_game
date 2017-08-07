#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
野村の証券用語集を掻き集めてくるスクリプト。

TODO: Dynamo DB に叩き込む
"""

import requests
from pyquery import PyQuery as pq

DEBUG = True


def get_pq(url):
    data = requests.get(url)
    data.encoding = 'utf-8'
    return pq(data.text)


def main():
    base_url = 'https://www.nomura.co.jp'
    url = base_url + '/terms/'

    urls = []
    table_page = get_pq(url)
    for item in table_page('.table_keyword a').items():
        urls.append(base_url + item.attr('href'))

    result = {}
    for url in urls:
        list_page = get_pq(url)
        for item in list_page('#content ul li').items():
            text = item('a').text()
            term_url = base_url + item('a').attr('href')
            term_page = get_pq(term_url)
            term_content = term_page('.term-content p').filter(
                lambda i, this: not pq(this).has_class('term-label')
            )
            result[item('a').text()] = term_content.text()

            if DEBUG:
                break

    if DEBUG:
        print(result)


if __name__ == "__main__":
    main()
