from flask import Flask, render_template
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import mysql.connector


def scrape_data(url):
    # Open the chrome web driver
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)

    # ensure the page loads image source (dynamic property)
    time.sleep(0.3)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    description_html = soup.find(class_="Text-yok90d-0 styles__DescriptionContainer-uwktmu-9 bWcgji")

    desc = description_html.contents[0].encode("ascii", "ignore").decode()
    desc = desc.replace("'", "")

    price_html = soup.find("span", {"data-testid": "fullPrice"})

    price = price_html.contents[0]

    img = soup.find("img", {"class": "styles__Image-uwktmu-7 cKdjfY LazyLoadImage__Image-sc-1732jps-1 cSwkPp"})

    src = img.get("src")

    # close the web driver
    driver.close()

    return "INSERT INTO products VALUES ('" + price + "', '" + src + "', '" + desc + "');"

    '''
        if soup.find("div", {"data-testid": "productPurchase"}).contents[0].contents[0] == "Sold":
            sold = "1"

        else:
            sold = "0"
    '''


def create_sql(username):

    commands = []

    home = "https://www.depop.com/" + username

    driver = webdriver.Chrome('./chromedriver')
    driver.get(home)

    time.sleep(1)

    elem = driver.find_element_by_tag_name("body")

    no_of_pagedowns = 100

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    urls = soup.find_all("a", {"data-testid" : "product__item"})

    for i in urls:
        commands.append((scrape_data("https://www.depop.com" + i.get("href"))))

    driver.close()

    return commands

class Pdf():

    def render_pdf(self, name, html):



        pdf = StringIO()

        pisa.CreatePDF(StringIO(html), pdf)

        return pdf.getvalue()


print("CREATE TABLE products (price varchar(255), src varchar(255), descr varchar(255), sold bit); ")

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


mydatabase = mysql.connector.connect(
    host = '127.0.0.1', user = 'root',
    passwd = 'password', database = 'testing')

mycursor = mydatabase.cursor()


@app.route('/button', defaults={'name': 'keef'})
@app.route('/button/<name>/')
def button(name):
    mycursor.execute('DELETE FROM products;')
    for command in create_sql(name) :
        print(command)
        mycursor.execute(command)
    mycursor.execute('SELECT * FROM products')
    data = mycursor.fetchall()
    html = render_template('stock.html', output_data=data)
    return html


if __name__ == '__main__':
    app.run()

