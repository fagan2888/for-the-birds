
import bs4
import datetime
import re
import requests

r = requests.get('http://ebird.org/ebird/printableList?regionCode=L1197287&yr=last10&m=8')
soup = bs4.BeautifulSoup(r.text, "lxml")

title = soup.select('.effortsubhead')[0].text
location, url, desc = [x.text for x in soup.select('.effortsub2head')]

location = location.replace('\n', ' ').replace('\t', '')

r = re.compile(r'[ /]')
fn = '%s.md' % r.sub('-', title)

blocks = soup.select('.block')[1:] # Skips first block---title, location, &c

with open(fn, 'w') as f:
    f.write('\n* %s\n\n' % title)
    f.write('    * %s\n' %  location)
    f.write('    * [`%s`](%s)\n' % (url, url))
    f.write('    * %s\n\n' % desc)

    for block in blocks:
        if block.text != '\n\n \n':
            if len(block) == 5:
                block = block.contents[1]
            for b in block.contents:
                if type(b) == bs4.element.Tag:
                    a = b.attrs
                    if a['class'][0] == 'item-heading':
                        f.write('\n## %s\n\n' % b.text)
                    elif a['class'][0] == 'subitem':
                         f.write('  * %s\n' % b.text)

    f.write('\nGenerated at %s\n\n' % datetime.datetime.today())

