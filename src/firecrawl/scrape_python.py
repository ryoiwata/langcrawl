# pip install firecrawl-py
from firecrawl import Firecrawl

app = Firecrawl(api_key="fc-c4914b55239c41b294ec14c3934944e7")

# Scrape a website:
app.scrape('firecrawl.dev')