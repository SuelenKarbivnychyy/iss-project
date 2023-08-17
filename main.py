import requests
from datetime import datetime
import smtplib
import config
import time

MY_LAT = 28.058570
MY_LONG = -82.689470


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"]) - 4
    iss_longitude = float(data["iss_position"]["longitude"]) - 4

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    else:
        return False


def send_email():
    """A function to send an email"""

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=config.my_email, password=config.password)
        connection.sendmail(
            from_addr=config.my_email,
            to_addrs=config.send_to,
            msg="Subject: Look To the sky\n\nHey, Its time to look up."
        )

    print("email sent")


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_utc = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    if sunset_utc == 0:
        sunset_florida = 20
    else:
        sunset_florida = sunset_utc - 4

    hour = datetime.now().hour
    if sunset_florida < hour < sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        send_email()
