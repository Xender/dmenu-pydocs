#!/usr/bin/env python3


# dmenu-pydocs -  dmenu-based Python library documentation search.
# Copyright (C) 2015  Aleksander Nitecki
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import subprocess
import urllib.parse

from collections import OrderedDict

from bs4 import BeautifulSoup


library_docs_index_url = 'file:///usr/share/doc/python/html/library/index.html'
# library_docs_index_url = 'https://docs.python.org/3/library/index.html'
# library_docs_index_url = 'https://docs.python.org/2/library/index.html'

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


def get_url(url):
	if url.startswith('file://'):
		with open(url[7:]) as f:
			return f.read()

	else:
		import requests  # Import conditionally for users who don't have it installed, but want to use local docs.

		response = requests.get(url)
		response.raise_for_status()

		return response.text


def main():
	library_docs_index = get_url(library_docs_index_url)
	soup = BeautifulSoup(library_docs_index, 'lxml')

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


	try:
		href = links[out]
	except KeyError:
		raise sys.exit(1)

	url = urllib.parse.urljoin(library_docs_index_url, href)
	print(url)


if __name__ == '__main__':
	main()
