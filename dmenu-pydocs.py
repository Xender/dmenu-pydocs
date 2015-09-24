#!/usr/bin/env python3

import sys
import subprocess
import urllib.parse

from collections import OrderedDict

from bs4 import BeautifulSoup


library_docs_index_path = '/usr/share/doc/python/html/library/index.html'

dmenu_cmd = [ 'dmenu',
	'-f',
	'-l',  '16',

	# '-nb', '#013',
	# '-nf', '#AAD',

	# '-nb', '#130',
	# '-nf', '#ADA',
	# '-sb', '#0A0',

	'-nb', '#320',
	'-nf', '#DBA',
	'-sb', '#A80',

	'-o',  '0.8',
]


def main():
	with open(library_docs_index_path) as library_docs_index:
		soup = BeautifulSoup(library_docs_index, "lxml")

	html_links = soup.select('li a')
	links = OrderedDict( (link.get_text(), link['href']) for link in html_links )


	with subprocess.Popen( dmenu_cmd,
		universal_newlines=True,
		stdin = subprocess.PIPE,
		stdout = subprocess.PIPE,
		stderr = sys.stderr
	) as dmenu:

		for link in links.keys():
			print(link, file=dmenu.stdin)

		out = dmenu.communicate()[0].strip()


	print(out)

	try:
		href = links[out]
	except KeyError:
		raise sys.exit(1)

	url = urllib.parse.urljoin(library_docs_index_path, href)
	print(url)


if __name__ == '__main__':
	main()
