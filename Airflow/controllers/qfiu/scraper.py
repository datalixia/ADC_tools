import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta


def get_page(page):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'fr-FR,fr;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://www.qfiu.gov.qa/?page_id=33',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        # 'Cookie': 'pll_language=en',
    }

    if page == 0:
        params = {
            'page_id': '33',
        }
    else:
        params = {
            'paged': str(page),
            'page_id': '33',
        }


    response = requests.get('https://www.qfiu.gov.qa/', params=params, headers=headers, verify=False)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.content,'lxml')
    links = soup.select(".read-more a")
    

    data = []
    for link in links:
        
        article_url = link['href']
        article_id = parse_qs(urlparse(article_url).query).get('p', [None])[0]

        article = {
            'id': article_id,
            'url' : article_url
        }

        article_content = get_article_content(article)
        
        data.append(article_content)

    
    return data
    try:
        
        pass
    except:
        return None
    




def get_article_content(article):
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'fr-FR,fr;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://www.qfiu.gov.qa/?paged=2&page_id=33',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    # 'Cookie': 'pll_language=en',
    }

    params = {
        'p': str(article['id']),
    }

    try:
        response = requests.get('https://www.qfiu.gov.qa/', params=params, headers=headers, verify=False)
        if response.status_code != 200:
           return None
        
        soup = BeautifulSoup(response.content,'lxml')
        title = soup.select_one('h1.entry-title').text
        content = soup.select_one('div.entry-content').text.strip().replace('\n',' ')
        timestamp = int(datetime.now().timestamp())

        article =  {
            'title' : title,
            'url' : article['id'],
            'content' : content,
            'date_time' : timestamp,
        }

        return article

    except:
        return None


def timestamp_ago(days):
    # Get current time
    now = datetime.now()

    # Subtract days
    time_days_ago = now - timedelta(days=days)

    # Convert to timestamp
    timestamp_days_ago = int(time_days_ago.timestamp())
    return int(timestamp_days_ago)


def main(limit_days, limit_articles, source):
    print("Scaping www.qfiu.gov.qa")
    data = []
    page = 1
    while True:

        print(f"Scaping www.qfiu.gov.qa : page {page}")
        end = False
        articles = get_page(page)

        # test empty article
        if len(articles) == 0:
            print(f"Scaping www.qfiu.gov.qa : no article")
            break

        for article in articles:

            time_article = article['date_time']
            time_ago = timestamp_ago(limit_days)

            if time_article < time_ago:
                print(f"Scaping www.qfiu.gov.qa : limit date reached")
                end = True
                break
            
            if len(data) > limit_articles:
                print(f"Scaping www.qfiu.gov.qa : limit number of articles reached")
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


