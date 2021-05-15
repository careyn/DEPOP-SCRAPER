from bs4 import BeautifulSoup
from selenium import webdriver
import time

# url of the page we want to scrape
url = "https://www.depop.com/products/shoppixelchick-reversible-pisces-pendant/"

# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome('./chromedriver')
driver.get(url)

# this is just to ensure that the page is loaded
time.sleep(3)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

descriptionHtml = soup.find(class_="Text-yok90d-0 styles__DescriptionContainer-uwktmu-9 bWcgji")

print(descriptionHtml.contents[0])

priceHtml = soup.find("span", {"data-testid" : "fullPrice"})

print(priceHtml.contents[0])

img = soup.find("img", {"class" : "styles__Image-uwktmu-7 cKdjfY LazyLoadImage__Image-sc-1732jps-1 cSwkPp"})

print(img.get("src"))

driver.close()