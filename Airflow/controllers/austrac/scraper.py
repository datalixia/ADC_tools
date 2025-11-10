import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def get_article_content(url,page):


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': f'https://www.austrac.gov.au/business/updates?page={page}',
        'Connection': 'keep-alive',
        # 'Cookie': 'ak_bmsc=3D29FA36916404925858B3ED3B357B0B~000000000000000000000000000000~YAAQN5MWArXxTEqUAQAAxbqeVRrLwEZzMtqBvP6ol7dzGUfQUQQXhNTBz3LecYBoijr8WN5V7J0iF0AywT1STDPbTWxuk1uJFGgaM+PRpFTRDqaTyEChQBKX+nyjMKAi4qBL+0j2i5ya0pk/POfdIeSpCo1dYK2ykWuHVB3AjisDmwPdFnz4ZyxoQWz4Yz+3qnWJ7XjHF0RLKZ1pXYp0JdN5h0XZTpLhqFc+DAv5NKuVGDEhsGlAxFxJUaJ9RM5AE4J8/KCzTiJEFsMAUebEhTv3W/cJwq2YXqYyRCb9Rnjs0PNwKw00dLbPMwIyJwEKYKzdvrq3jbYGBHV0m0irCxc9TgE7J8C2HMp9JRkz4dAcEF92RAYQpv1BuX6Nz3Ib9ZOc5ozxPpWOnynAQCbpIwiOCq/iZ3fnb7jLGQF90jydi/I7UFDdhg6cObSle4rqvZLnyqBowiT1s4rqJI/gbw==; _ga_2PDVTFHRNK=GS1.1.1736603251.1.1.1736603588.0.0.0; _ga=GA1.3.286124867.1736603251; _ga_0XT7NFV9ZS=GS1.1.1736603252.1.1.1736603588.0.0.0; _gid=GA1.3.1119781484.1736603253; bm_sv=2555149447E6C11A32069B01310EA3F9~YAAQFPsUAgiJ26+TAQAAXrOjVRqXzi7oDuPEWLM7kYh8fspUam0ZmElpKf6rbRmAYumYysZdQTbEashftOCEzHn0PzTkVuuwYk/65v7dda90ToHzDLBBgUBFUCQfSbHQQ+frFxS+i5+1INYFk7D/9sknS//m337PzwGVNCM1xk+BcfKZtWCb3taApWwGZlEjru8zXU9NL4QaFhHirXYh3IiwVd9uNATGreD3Xg7v7X1kAqY9LaonBhSy03mkXYvwkfveew==~1',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'If-Modified-Since': 'Sat, 11 Jan 2025 13:52:58 GMT',
        'If-None-Match': '"1736603578"',
        'Priority': 'u=0, i',
    }

    response = requests.get(
        url,
        headers=headers,
    )

    soup = BeautifulSoup(response.content,'lxml')
    content = soup.select_one('div.container.body-copy').get_text()

    return content


def get_page(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'Referer': 'https://www.austrac.gov.au/business/updates',
        # 'Cookie': 'ak_bmsc=3D29FA36916404925858B3ED3B357B0B~000000000000000000000000000000~YAAQN5MWArXxTEqUAQAAxbqeVRrLwEZzMtqBvP6ol7dzGUfQUQQXhNTBz3LecYBoijr8WN5V7J0iF0AywT1STDPbTWxuk1uJFGgaM+PRpFTRDqaTyEChQBKX+nyjMKAi4qBL+0j2i5ya0pk/POfdIeSpCo1dYK2ykWuHVB3AjisDmwPdFnz4ZyxoQWz4Yz+3qnWJ7XjHF0RLKZ1pXYp0JdN5h0XZTpLhqFc+DAv5NKuVGDEhsGlAxFxJUaJ9RM5AE4J8/KCzTiJEFsMAUebEhTv3W/cJwq2YXqYyRCb9Rnjs0PNwKw00dLbPMwIyJwEKYKzdvrq3jbYGBHV0m0irCxc9TgE7J8C2HMp9JRkz4dAcEF92RAYQpv1BuX6Nz3Ib9ZOc5ozxPpWOnynAQCbpIwiOCq/iZ3fnb7jLGQF90jydi/I7UFDdhg6cObSle4rqvZLnyqBowiT1s4rqJI/gbw==; _ga_2PDVTFHRNK=GS1.1.1736603251.1.1.1736603305.0.0.0; _ga=GA1.3.286124867.1736603251; _ga_0XT7NFV9ZS=GS1.1.1736603252.1.1.1736603305.0.0.0; _gid=GA1.3.1119781484.1736603253; bm_sv=2555149447E6C11A32069B01310EA3F9~YAAQN5MWAmT6TEqUAQAALXufVRoCZyNqNAbYtK0b1v8NNTOiMKsfFyLZn0bP1rGLJrvSXyavnaTYASS/4/Q+wefQFCNGvByBqfaeAdHPSzJUE4TQxl0XYCX75OnLR561N7grY1Ycuy6EZU/yOuEOkEhLzYjBRz89JOK5MDqWuGm6XVi9wLTxrq+BsugQZLtqFFPjJUvPfJpuXPxRFEDYELwljvMmXs3MWF9ZIlZCyp7LmF7O1fKtdC7y3rdYP4U6yDmCqQ==~1',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        'page': page,
    }

    response = requests.get('https://www.austrac.gov.au/business/updates', params=params, headers=headers)
    soup = BeautifulSoup(response.content,'lxml')
    articles = soup.select('div.latest-news__card')

    data = []
    for article in articles:
        title = article.select_one("a.latest-news__card-title").text
        url = article.select_one("a.latest-news__card-title")['href']
        date_time = article.select_one('time')['datetime']
        content = get_article_content(url,1)
        
        data.append({
            'title' : title,
            'url' : url,
            'content' : content,
            'date_time' : string_to_timestamp(date_time)
        })

    return data


def string_to_timestamp(iso_string):
    try:
        dt = datetime.fromisoformat(iso_string)  # Parses the ISO 8601 string
        timestamp = dt.timestamp()
        return int(timestamp)
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
    print("Scaping austrac.gov.au")
    page = 0
    data = []
    while True:
        print(f"Scaping austrac.gov.au : page {page}")
        end = False
        articles = get_page(page)
        
        # test empty article
        if len(articles) == 0:
            print(f"Scaping austrac.gov.au : no article")
            break

        # test date reached
        for article in articles:
            
            time_article = article['date_time']
            time_ago = timestamp_ago(limit_days)

            if time_article < time_ago:
                print(f"Scaping austrac.gov.au : limit date reached")
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

