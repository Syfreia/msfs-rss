from bs4 import BeautifulSoup
import requests
from feedgen.feed import FeedGenerator
from datetime import datetime

main_url = 'https://fselite.net/simulator/msfs/'
rss_url = 'https://raw.githubusercontent.com/evroon/msfs-rss/main/feeds/msfs.xml'

# Initialize RSS feed.
fg = FeedGenerator()
fg.id(main_url)
fg.title('MSFS Blog')
fg.subtitle('Development updates of Microsoft Flight Simulator.')
fg.link(href=main_url, rel='alternate')
fg.logo('https://msfs-cdn.azureedge.net/wp-content/uploads/2020/03/msf-logo.png')
fg.link(href=rss_url, rel='self')
fg.language('en')

page = requests.get(main_url)
soup = BeautifulSoup(page.text, 'html.parser')

# Update the class names to match the structure of the new website
posts = soup.find_all(class_='brxe-block')

# Add blog post entries to feed.
for post in posts:
    # Update the class names to match the structure of the new website
    header = post.find(class_='brxe-heading')
    summary = post.find(class_='excerpt-text')
    meta = post.find(class_='brxe-text-basic')
    image = post.find(class_='css-filter')

    title = header.text.strip()
    url = header.find('a')['href']
    body = summary.text.strip()
    date = datetime.fromisoformat(meta.find('time')['datetime'])

    fe = fg.add_entry()
    fe.id(url)
    fe.title(title)
    fe.link(href=url)
    fe.pubDate(date)
    fe.updated(date)
    fe.summary(body)
    
    if image is not None:
        enclosure = image['src']
        img_headers = requests.head(enclosure).headers
        fe.enclosure(enclosure, img_headers['content-length'], img_headers['content-type'])

fg.atom_file('feeds/msfs_extra.xml', pretty=True)