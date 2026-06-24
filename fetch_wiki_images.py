import requests

headers = {'User-Agent': 'RyderProBot/1.0 (https://ryderpro.com)'}

def get_wiki_images(title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&prop=images&format=json"
    res = requests.get(url, headers=headers).json()
    pages = res['query']['pages']
    for page_id in pages:
        for img in pages[page_id].get('images', []):
            img_title = img['title']
            if '.jpg' in img_title.lower() or '.png' in img_title.lower():
                img_url_req = f"https://en.wikipedia.org/w/api.php?action=query&titles={img_title}&prop=imageinfo&iiprop=url&format=json"
                img_res = requests.get(img_url_req, headers=headers).json()
                img_pages = img_res['query']['pages']
                for ipage_id in img_pages:
                    url_info = img_pages[ipage_id].get('imageinfo', [{}])[0].get('url')
                    if url_info:
                        print(f"{url_info}")

get_wiki_images('Porsche_911_GT3')
get_wiki_images('Rolls-Royce_Cullinan')
