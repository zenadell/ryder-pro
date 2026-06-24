from duckduckgo_search import DDGS

with DDGS() as ddgs:
    results = ddgs.images("site:unsplash.com porsche 911", max_results=3)
    for r in results:
        print(r['image'])
