from bs4 import BeautifulSoup
import requests
import lxml,json
import pandas as pd

df = pd.DataFrame(columns = ['Image', 'Name', 'URL','Metascore','Userscore','Platform', 'Summary'])

def export_data(df):
  df.to_csv('data.csv')


base_url = 'https://www.metacritic.com/browse/games/release-date/available/pc/metascore'
#user_agent = {'User-agent': 'Mozilla/5.0'}

def get_data(base_url, user_agent = {'User-agent': 'Mozilla/5.0'}):
  base = requests.get(base_url,headers=user_agent)
  bs = BeautifulSoup(base.text, 'lxml')

  for tr1 in bs.find_all("tr", {'class':'spacer'}):              #removing extra <tr>
      tr1.decompose()

  games = bs.find_all('tr')                                      #find all rows
  df_temp = pd.DataFrame(columns = ['Image', 'Name', 'URL','Metascore','Userscore','Platform', 'Summary'])
  for row_data in games:
      name = row_data.find('h3').text
      platform = row_data.find('span', class_='data').text.strip()
      summary = row_data.find('div', class_ = 'summary').text.strip()
      metascore = row_data.find('div', class_ = 'metascore_w large game positive').text.strip()
      userscore = row_data.find('div', class_ = 'clamp-userscore').div.text.strip()
      url = row_data.find('a', href = True, class_ = 'title')
      image = row_data.find('img', src = True)
      #release = row_data.find('span', class_ = 'clamp-details')
      df_temp = df_temp.append({'Image' : image['src'], 'Name' :name, 'URL' : url['href'], 'Metascore' : metascore, 'Userscore' : userscore, 'Platform' : platform, 'Summary': summary},  ignore_index = True)
      print(f"Name: {name}")
      print(f"Metascore: {metascore}")
      print(f"User Score: {userscore}")
      print(f"Platform: {platform}")
      print(f"URL: https://www.metacritic.com{url['href']}")
      print(f"Image_URL: {image['src']}")
      #print(f"Release: {release}")
      print(f"Summary: {summary}\n")
  
  return df_temp

df = df.append(get_data(base_url))

df.head()