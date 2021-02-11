from bs4 import BeautifulSoup
import requests
import lxml,json
import pandas as pd

df = pd.DataFrame(columns = ['Image_url', 'Name', 'URL','Metascore','Userscore','Platform', 'Summary','Developer', 'Genre', 'Rating', 'Release'])

def export_data(df):
  df.to_csv('Data/data.csv',encoding='utf-8', index=False)
  print("done")

base_df = pd.read_csv('Data\data.csv')
#base_df.head()



base_url = 'https://www.metacritic.com/game/pc/grand-theft-auto-v'
user_agent = {'User-agent': 'Mozilla/5.0'}

base = requests.get(base_url,headers=user_agent)
bs = BeautifulSoup(base.text, 'lxml')



soup = bs.find('div', class_ = 'product_title')
name = soup.find('a', class_ = 'hover_none').text.strip()
print(name)



soup = bs.find('li', class_ = 'summary_detail publisher')
publisher = soup.find('span', class_='data').a.text.strip()
print(publisher)



soup = bs.find('li', class_='summary_detail release_data')
release = soup.find('span', class_='data').text.strip()
print(release)



platform =[]
platform_1 = bs.find('span', class_ = 'platform').a.text.replace(' ','').strip()
platform.append(platform_1)
soup = bs.find('li', class_ = 'summary_detail product_platforms')
if soup != None:
    platform_soup = soup.find_all('a', class_='hover_none')
    for i in platform_soup:
        platform.append(i.text)
    print(type(platform))

print(platform)



summary = bs.find('span', class_ = 'blurb blurb_expanded').text
if summary == None:
    summary = bs.find('span', class_ = 'blurb blurb_collapsed').text
print(summary)


metascore = bs.find('a', class_ = 'metascore_anchor').span.text
print(metascore)



userscore = bs.find('div', class_ = 'userscore_wrap feature_userscore').a.div.text
print(userscore)


url = bs.find('div', class_ = 'product_title').a['href']
url = 'https://www.metacritic.com' + url
print(url)

image_url = bs.find('img', class_='product_image large_image')['src']
print(image_url)


soup = bs.find('li', class_ = 'summary_detail product_rating')
if soup == None:
    rating = 'None'
rating = soup.find('span', class_='data').text
print(rating)

soup = bs.find('li', class_ = 'summary_detail product_genre')
genre = []
if soup == None:
    genre = 'NA'
for i in soup.find_all('span', class_ ='data'):
    genre.append(i.text)
print(genre)


print(f"Name: {name}")
print(f"Publisher: {publisher}")
print(f"Release: {release}")
print(f"Rating: {rating}")
print(f"Genre(s): {genre}")
print(f"Platform(s): {platform}")
print(f"Metascore: {metascore}")
print(f"Userscore: {userscore}")
print(f"Image_URL: {image_url}")
print(f"URL: {url}")
print(f"Summary: {summary}\n")




