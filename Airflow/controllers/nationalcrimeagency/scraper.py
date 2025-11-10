import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def get_article_content(url,page):

    base_url = "https://www.nationalcrimeagency.gov.uk"

    if(page == 0):
        refer_url = f'https://www.nationalcrimeagency.gov.uk/news'
        
    else:
        refer_url = f'https://www.nationalcrimeagency.gov.uk/news?start={str(page*16)}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': refer_url,
        'Connection': 'keep-alive',
        # 'Cookie': 'CookieControl={"necessaryCookies":[],"optionalCookies":{},"statement":{},"consentDate":1736605141110,"consentExpiry":90,"interactedWith":true,"user":"0079DB28-06E7-42ED-82F2-C9E07E20D3F3"}',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    

    response = requests.get(
        base_url+url,
        headers=headers,
    )

    soup = BeautifulSoup(response.content,'lxml')
    content = soup.select_one('div[itemprop="articleBody"]').get_text()
    date_time = soup.select_one('div[itemprop="articleBody"] p:last-child').get_text()

    return date_time, content




def get_page(page):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'Referer': 'https://www.nationalcrimeagency.gov.uk/news',
        # 'Cookie': 'CookieControl={"necessaryCookies":[],"optionalCookies":{},"statement":{},"consentDate":1736605141110,"consentExpiry":90,"interactedWith":true,"user":"0079DB28-06E7-42ED-82F2-C9E07E20D3F3"}',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    if(page == 0):
        response = requests.get(
            'https://www.nationalcrimeagency.gov.uk/news', 
            headers=headers
            )
    else:
        params = {
            'start': str(page*16),
        }

        response = requests.get(
            'https://www.nationalcrimeagency.gov.uk/news', 
            params=params, 
            headers=headers
            )

    soup = BeautifulSoup(response.content,'lxml')
    articles = soup.select('div.items-row')
    if(len(articles) == 0):
        return []
    first_articles = soup.select_one('div.items-leading')

    articles.insert(0,first_articles)
    

    data = []
    for article in articles:
        title = article.select_one('.page-header a').text.strip()
        url = article.select_one('.page-header a')['href']
        date_time, content = get_article_content(url, page)
        data.append({
            'title' : title,
            'url' : f"https://www.nationalcrimeagency.gov.uk{url}",
            'content' : content,
            'date_time' : string_to_timestamp(date_time)
        })

    return data


def string_to_timestamp(iso_string):
    try:
        datetime_obj = datetime.strptime(iso_string, "%d %B %Y").replace(hour=12, minute=0, second=0)
        timestamp = int(datetime_obj.timestamp())
        return timestamp
    except:
        timestamp = int(datetime.now().timestamp())
        return int(timestamp)


def timestamp_ago(days):
    # Get current time
    now = datetime.now()

    # Subtract days
    time_days_ago = now - timedelta(days=days)

    # Convert to timestamp
    timestamp_days_ago = int(time_days_ago.timestamp())
    return int(timestamp_days_ago)

def main(limit_days, limit_articles, source):
    print("Scaping nationalcrimeagency")
    page = 0
    data = []
    while True:
        print(f"Scaping nationalcrimeagency : page {page}")
        end = False
        articles = get_page(page)

        # test empty article
        if len(articles) == 0:
            print(f"Scaping nationalcrimeagency : no article")
            break

        # test date reached
        for article in articles:

            time_article = article['date_time']
            time_ago = timestamp_ago(limit_days)

            if time_article < time_ago:
                print(f"Scaping nationalcrimeagency : limit date reached")
                end = True
                break
            
            if len(data) > limit_articles:
                print(f"Scaping nationalcrimeagency : limit number of articles reached")
                end = True
                break

            article['source_id'] = source['id']
            article['source_name'] = source['name']
            article['read'] = False
            
            data.append(article)

        if end == True:
            break

        page = page + 1

    return data