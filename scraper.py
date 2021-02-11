from bs4 import BeautifulSoup
import requests
import lxml,json
import pandas as pd



df = pd.DataFrame(columns = ['Image', 'Name', 'URL','Metascore','Userscore','Platform', 'Summary'])

base_url = 'https://www.metacritic.com/browse/games/release-date/available/pc/metascore'
user_agent = {'User-agent': 'Mozilla/5.0'}

base = requests.get(base_url,headers=user_agent)
bs = BeautifulSoup(base.text, 'lxml')

for tr1 in bs.find_all("tr", {'class':'spacer'}):              #removing extra <tr>
    tr1.decompose()

games = bs.find_all('tr')                                      #find all rows

for row_data in games:
    name = row_data.find('h3').text
    platform = row_data.find('span', class_='data').text.strip()
    summary = row_data.find('div', class_ = 'summary').text.strip()
    metascore = row_data.find('div', class_ = 'metascore_w large game positive').text.strip()
    userscore = row_data.find('div', class_ = 'clamp-userscore').div.text.strip()
    url = row_data.find('a', href = True, class_ = 'title')
    image = row_data.find('img', src = True)
    #release = row_data.find('span', class_ = 'clamp-details')
    df = df.append({'Image' : image['src'], 'Name' :name, 'URL' : url['href'], 'Metascore' : metascore, 'Userscore' : userscore, 'Platform' : platform, 'Summary': summary},  ignore_index = True)
    print(f"Name: {name}")
    print(f"Metascore: {metascore}")
    print(f"User Score: {userscore}")
    print(f"Platform: {platform}")
    print(f"URL: https://www.metacritic.com{url['href']}")
    print(f"Image_URL: {image['src']}")
    #print(f"Release: {release}")
    print(f"Summary: {summary}\n")

df.head()
#########################################################################################################
soup = bs.find_all('table', class_='clamp-list')
names_list = bs.find_all('a', class_='title')

for names in names_list:
    name = names.find('a').text
    print(f"Name: {name.strip()}")

print(names)
#print(base.text)
# Checking if we successfully fetched the URL
if base.status_code == requests.codes.ok:
  bs = BeautifulSoup(base.text, 'lxml')
  # Fetching all items
  list_all_games = bs.findAll('table', class_='clamp-list')
  data = {
    'Image': [],
    'Name': [],
    'URL': [],
    'Artist': [],
    'Binding': [],
    'Format': [],
    'Release Date': [],
    'Label': [],
  }
  
  for cd in list_all_cd:

    # Getting the CD attributes
    image = cd.find('img', class_='ProductImage')['src']

    name = cd.find('h2').find('a').text

    url = cd.find('h2').find('a')['href']
    url = base_url + url

    artist = cd.find('li', class_="Artist")
    artist = artist.find('a').text if artist else ''

    binding = cd.find('li', class_="Binding")
    binding = binding.text.replace('Binding: ', '') if binding else ''

    format_album = cd.find('li', class_="Format")
    format_album = format_album.text.replace('Format: ', '') if format_album else ''

    release_date = cd.find('li', class_="ReleaseDate")
    release_date = release_date.text.replace('Released: ', '') if release_date else ''

    label = cd.find('li', class_="Label")
    label = label.find('a').text if label else ''

    # Store the values into the 'data' object
    data['Image'].append(image)
    data['Name'].append(name)
    data['URL'].append(url)
    data['Artist'].append(artist)
    data['Binding'].append(binding)
    data['Format'].append(format_album)
    data['Release Date'].append(release_date)
    data['Label'].append(label)

  table = pd.DataFrame(data, columns=['Image', 'Name', 'URL', 'Artist', 'Binding', 'Format', 'Release Date', 'Label'])
  table.index = table.index + 1
  table.to_csv(f'{band_name}_albums.csv', sep=',', encoding='utf-8', index=False)
  print(table)