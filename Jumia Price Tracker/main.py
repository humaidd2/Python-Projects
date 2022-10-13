import requests
from bs4 import BeautifulSoup
import smtplib

SITE_LINK = "https://www.jumia.com.ng/generic-sets-of-kitchen-knives-sharpener-chopping-board-90517143.html"

response = requests.get(url=SITE_LINK)
amazon_site = response.text

soup = BeautifulSoup(amazon_site, "html.parser")


knife_site = soup.find(name="span", class_="-b -ltr -tal -fs24").text.split()[1].replace(",", "")
price = int(knife_site)

if price < 6000:
    with smtplib.SMTP("mail.gmail.com") as connection:
        connection.login(user="your_email", password="password")
        connection.starttls()
        connection.sendmail(
            from_addr="youremail@gmail.com",
            to_addrs="email@gmail.com",
            msg="Knife Under Price\n\n"
                f"Hey, Knife on jumaia is now N{price}\n\n"
                f"go ahead to this link to purchase it \n\n"
                f"{SITE_LINK}")
