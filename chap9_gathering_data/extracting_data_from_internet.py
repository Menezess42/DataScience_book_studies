# Doing this is easy, but getting structured and meaningful
# data is another story.

# We gonna Beautifulsoup builds a tree with the various elemnts of HTML and
# gives a simples interface to access.
# We also will use the Requests library. A simpler way to do HTTP Requests.

# The Python default HTML analayser is not so good. So we will use the html5lib.

# To use Beautifulsoup, we pass a string with HTMl to the Beautifulsoup function.
# In the examples this will be a requests.get call

from bs4 import BeautifulSoup
import requests

class JustShowing:
# Put the HTML file on GitHub.
    url = 'https://raw.githubusercontent.com/joelgrus/data/master/getting-data.html'
#url = 'https://raw.githubsercontent.com/joelgrus/data/master/getting-data.html'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')

# To find the first <p> tag (and it content), do this:
    first_paragraph = soup.find('p') # or just soup.p

# To obtain the content of the text of a Tag, use the property
# text:

    first_paragraph_text = soup.p.text
    first_paragraph_text = soup.p.text.split()

# And, to extract the atributes from a Tag, treate as a dict:
    first_paragraph_id = soup.p['id'] # genarates a keyError if no id
    first_paragraph_id2= soup.p.get('id') # Returns None if has no id

# To obtain multiple tags at same time:
    all_paragraphs = soup.find_all('p') # or just soup('p')
    paragraphs_with_ids = [p for p in soup('p') if p.get('id')]

# Many times you will have to find tags iwth specific class
    important_paragraph = soup('p', {'class': 'important'})
    important_paragraph2 = soup('p', 'important')
    important_paragraph3 = [p for p in soup('p')
                            if 'important' in p.get('class', [])]


# More elaborated implementation.
# Example, to find all the elements <span> in a element <div>, we do:
# Warning: Will return the same <span> multiple time if it in various <div>
    spans_inside_divs = [span for div in soup('div') # for each <div> in the page
                         for span in div('span')] # find each <span> inside.


# In general, the important data will not be label as class='important'.
# It is necessary analayse the HTML, the selection logic and the extrem
# cases to confirm if the data is correct. Let's to an exemplo.

# *Exemple: Monitoring the congress*
# You have to identify all the congressman that
# the press release mentioned the word 'data'.

# When we see the raw HTML, the links show as follows:
'''
<td>
    <a href='https://alugumaCoisa.gov'>Jayapal, Pramila </a>
</td>
'''

# We start colecting all the URLs with links on the page:

url = 'https://www.house.gov/representatives'
text = requests.get(url).text
soup = BeautifulSoup(text, 'html5lib')

all_urls = [a['href']
            for a in soup('a')
            if a.has_attr('href')]

print(len(all_urls)) # 967 is to mutch

# This returns to mutch URLs. We want the ones
# that start with http:// or https://, has a name
# and ends with .house.gov or house.gov/.

# It's a good oportunity to use a regular expression
import re

# Must start with http:// or https://
# Must end with .house.gov or .house.gov/
regex = r'^https?://.*\.house\.gov/?$'

# Let's write some tests
assert re.match(regex, 'http://joel.house.gov')
assert re.match(regex, 'https://joel.house.gov')
assert re.match(regex, 'http://joel.house.gov/')
assert re.match(regex, 'https://joel.house.gov/')
assert not re.match(regex, 'http://joel.house.com')
assert not re.match(regex, 'http://joel.house.gov/biography')

# Now, insert
good_urls = [url for url in all_urls if re.match(regex, url)]

print(len(good_urls)) # 876

# The result still surpass the 435 parliamentarians, because the list
# has duplicated values. For clean that we use set:
good_urls = list(set(good_urls))

print(len(good_urls)) # just 438 for me

from typing import Dict, Set

press_releases: Dict[str, Set[str]] = {}
for i, house_url in enumerate(good_urls):
    html = requests.get(house_url).text
    soup = BeautifulSoup(html, 'html5lib')
    pr_link = {a['href'] for a in soup('a') if 'press releases' in a.text.lower()}
    press_releases[house_url] = pr_link
    print(i)
    if i == 50:
        break


# In the website's source code, we see that there is a snippet
# of each announcement in a <p> tag, so we'll use that on the
# first try:
def paragraph_mentions(text: str, keyword: str) -> bool:
    '''
    Returns True if <p> in the mentioned text {keyword}
    '''
    soup = BeautifulSoup(text, 'html5lib')
    paragraphs = [p.get_text() for p in soup('p')]
    print('entrou')
    return any(keyword.lower() in paragraph.lower()
               for paragraph in paragraphs)

# Let's write some basic tests
text = """<body><h1>Facebook</h1><p>Twitter</p>"""
assert paragraph_mentions(text, 'Twitter') # it is on a <p>
assert not paragraph_mentions(text, 'facebook') # it is not in a <p>

# Now we are ready to find the correct parliamentarians and
# inform their names to the vice-president
for house_url, pr_links in press_releases.items():
    print('aaaaa')
    for p_link in pr_links:
        print('bbbbb')
        url = f'{house_url}/{pr_links}'
        text = requests.get(url).text
        if paragraph_mentions(text, 'data'):
            print(f'{house_url}')
            break # end of the activitie in house_url
