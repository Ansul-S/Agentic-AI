from src.tools.tools import scrape_url

results = scrape_url.invoke({
    "url": "https://www.formula1.com/"
})

print(results)