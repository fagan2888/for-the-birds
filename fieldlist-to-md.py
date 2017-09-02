
import bs4
import datetime
import re
import requests

r = requests.get('http://ebird.org/ebird/printableList?regionCode=L285216&yr=last10&m=9')

soup = bs4.BeautifulSoup(r.text, "lxml")

title = soup.select('.effortsubhead')[0].text
location, url, desc = [x.text for x in soup.select('.effortsub2head')]

location = location.replace('\n', ' ').replace('\t', '')

r = re.compile(r'[ /]')
fn = '%s.md' % r.sub('-', title)

blocks = soup.select('.block')[1:] # Skips first block---title, location, &c

with open(fn, 'w') as f:
    f.write('''
---
fontsize: 10pt
geometry: margin=1in
header-includes:
    - \\usepackage{multicol}
    - \\newcommand{\\hideFromPandoc}[1]{#1}
    - \\hideFromPandoc{
        \\let\\Begin\\begin
        \\let\\End\\end
      }
---
''')
    f.write('\n# %s\n\n' % title)
    f.write('* %s\n' %  location)
    f.write('* [`%s`](%s)\n' % (url, url))
    f.write('* %s\n' % desc)
    f.write('\n-----\n\n\Begin{multicols}{3}\n\n')

    for block in blocks:
        if block.text != '\n\n \n':
            if len(block) == 5:
                block = block.contents[1]
            for b in block.contents:
                if type(b) == bs4.element.Tag:
                    a = b.attrs
                    if a['class'][0] == 'item-heading':
                        f.write('* **%s**\n' % b.text)
                    elif a['class'][0] == 'subitem':
                         f.write('    * %s\n' % b.text)

    f.write('\n\End{multicols}')
    f.write('\nGenerated at %s\n\n' % datetime.datetime.today())

