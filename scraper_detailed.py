#from _typeshed import NoneType
from bs4 import BeautifulSoup
import requests
import lxml,json
import pandas as pd

def export_data(df):
  df.to_csv(r'Data\data_extra.csv',encoding='utf-8',mode='a', index=False)
  print("done")

df = pd.DataFrame(columns = ['Image_url', 'Name', 'Publisher','Release','Rating','Genre','URL', 'Metascore','Userscore','Platform', 'Summary'])
base_df = pd.read_csv('Data\data.csv')


def scrappy(base_url):
    
    user_agent = {'User-agent': 'Mozilla/5.0'}

    base = requests.get(base_url,headers=user_agent)
    bs = BeautifulSoup(base.text, 'lxml')
    if base.status_code == 200:


        soup = bs.find('div', class_ = 'product_title')
        name = soup.find('a', class_ = 'hover_none').text.strip()
        #print(name)



        soup = bs.find('li', class_ = 'summary_detail publisher') if bs.find('li', class_ = 'summary_detail publisher') else 'None'
        publisher = "None"
        if soup != 'None':
            publisher = soup.find('span', class_='data').a.text.strip()
            #print(publisher)



        soup = bs.find('li', class_='summary_detail release_data') if bs.find('li', class_='summary_detail release_data') else 'None'
        if soup != 'None':
            release = soup.find('span', class_='data').text.strip()
            #print(release)



        platform =[]
        platform_1 = bs.find('span', class_ = 'platform').a.text.replace(' ','').strip()
        platform.append(platform_1)
        soup = bs.find('li', class_ = 'summary_detail product_platforms') if bs.find('li', class_ = 'summary_detail product_platforms') else 'None'
        if soup != 'None':
            platform_soup = soup.find_all('a', class_='hover_none')
            for i in platform_soup:
                platform.append(i.text)
            #print(type(platform))

        #print(platform)



        summary = bs.find('span', class_ = 'blurb blurb_expanded').text if bs.find('span', class_ = 'blurb blurb_expanded') else 'None'
        if summary == 'None':
            summary = bs.find('span', class_ = 'blurb blurb_collapsed').text if bs.find('span', class_ = 'blurb blurb_collapsed') else 'None'
            if summary == 'None':
                summary = bs.find('ul', class_ = 'summary_details')
                summary = bs.find('li', class_ ='summary_detail product_summary') if  bs.find('li', class_ ='summary_detail product_summary') else 'None'
                if summary != 'None':
                    summary = summary.find('span', class_ = 'data').text
                else:
                    summary = 'None'
        #print(summary)

        soup = bs.find('div', class_ = 'metascore_wrap highlight_metascore')
        metascore = "None" if soup.find('div', class_ ='data metascore connect4') else soup.find('a', class_ = 'metascore_anchor')
        #metascore = soup.find('a', class_ = 'metascore_anchor') if bs.find('a', class_ = 'metascore_anchor') else 'None'
        if metascore != 'None':
            metascore = metascore.text.split()
        

        userscore = bs.find('div', class_ = 'userscore_wrap feature_userscore').a.div.text if bs.find('div', class_ = 'userscore_wrap feature_userscore') else 'None'
        #print(userscore)


        url = bs.find('div', class_ = 'product_title').a['href']
        url = 'https://www.metacritic.com' + url
        #print(url)

        image_url = bs.find('img', class_='product_image large_image')['src'] if bs.find('img', class_='product_image large_image')['src'] else 'None'
        #print(image_url)

        soup = bs.find('li', class_ = 'summary_detail product_rating') if bs.find('li', class_ = 'summary_detail product_rating') else 'None'
        rating = 'None'
        if soup != 'None':
            rating = soup.find('span', class_='data').text.split()
            #print(rating)

        soup = bs.find('li', class_ = 'summary_detail product_genre') if bs.find('li', class_ = 'summary_detail product_genre') else 'None'
        genre = []
        if soup != 'None':
            for i in soup.find_all('span', class_ ='data'):
                genre.append(i.text)
            #print(genre)


        df_temp = pd.DataFrame(columns = ['Image_url', 'Name', 'Publisher','Release','Rating','Genre','URL', 'Metascore','Userscore','Platform', 'Summary'])
        df_temp = df_temp.append({'Image_url' : image_url , 'Name' :name , 'Publisher':publisher , 'Release': release , 'Rating': rating, 'Genre': genre, 'URL' : url,
                                'Metascore' : metascore, 'Userscore' : userscore, 'Platform' : platform, 'Summary': summary, },  ignore_index = True)
        '''print(f"Name: {name}")
        print(f"Publisher: {publisher}")
        print(f"Release: {release}")
        print(f"Rating: {rating}")
        print(f"Genre(s): {genre}")
        print(f"Platform(s): {platform}")
        print(f"Metascore: {metascore}")
        print(f"Userscore: {userscore}")
        print(f"Image_URL: {image_url}")
        print(f"URL: {url}")
        print(f"Summary: {summary}\n")'''
        return df_temp
    else:
        df_temp = pd.DataFrame(columns = ['Image_url', 'Name', 'Publisher','Release','Rating','Genre','URL', 'Metascore','Userscore','Platform', 'Summary'])
        df_temp = df_temp.append({'Image_url' : 'None' , 'Name' :'None' , 'Publisher':'None' , 'Release': 'None' , 'Rating': 'None', 'Genre':'None', 'URL' : 'None',
                                'Metascore' :'None', 'Userscore' : 'None', 'Platform' :'None', 'Summary': 'None', },  ignore_index = True)


'''df = df.append(scrappy(base_url = 'https://www.metacritic.com/game/pc/memento-mori-2'))
#df['Name'].iloc[-1]
df.head()'''

#df['Name'].iloc[-1]

count = 0
for i in base_df['URL'][0:]:
    df = df.append(scrappy(base_url = str(i)))
    count+=1
    print(count)

print(count)
df.tail()

export_data(df)