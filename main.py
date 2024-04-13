import requests
from datetime import datetime
import smtplib

MY_LAT = 40.188526
MY_LONG = 29.060965
parameters = {
    "lat":MY_LAT,
    "lng":MY_LONG,
    "formatted":0,
    "tzid":"Europe/Istanbul"
}

#---------------- gün doğum ve batış saatlerini api ile çekiyoruz.-------------
response = requests.get("https://api.sunrise-sunset.org/json",params=parameters)

sunrise = response.json()["results"]["sunrise"].split("T")[1].split(":")
sunset = response.json()["results"]["sunset"].split("T")[1].split(":")

sun_data=[]
for i,j in sunrise[0:2],sunset[0:2]:
    sun_data.append([int(i),int(j)])

saat = datetime.now()
suan=[saat.hour,saat.minute]

#---------------havanın karanlık olup olmadığını gözlemliyoruz----------------
karanlik_kontrol=0
if not sun_data[0][0] < suan[0] < sun_data[1][0]:

    if sun_data[0][0] == suan[0]:
        if sun_data[0][1] >= suan[1]:
            karanlik_kontrol=1
    elif sun_data[1][0] == suan[0]:
        if sun_data[1][1] <= suan[1]:
            karanlik_kontrol=1
    else:
        karanlik_kontrol=1

#--------------------ISS'in koordinatlarını tespit ediyoruz-------------------
coordinate = requests.get("http://api.open-notify.org/iss-now.json")
ISS = [coordinate.json()["iss_position"]["longitude"],coordinate.json()["iss_position"]["latitude"]]

#test
#karanlik_kontrol=1
#ISS = [29,40]

#---------ISS'in Bursa'nın üstünden geçip geçmediğini kontrol ediyoruz---------
def yakinlik_tespiti(sayi1,sayi2,esik_degeri):
    if abs(sayi1 - sayi2) < esik_degeri:
        return True

#---------hava karanlık ve ISS bursanın üstünden geçiyorsa mail atacak--------
def mail_at(baslik,icerik):

    email = "****"
    password = "****"

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(from_addr=email, to_addrs="****",
                            msg=f"Subject:{baslik}\n\n{icerik}")


if karanlik_kontrol==1:
    print(round(float(ISS[1]),1),round(float(ISS[0]),1))
    if (yakinlik_tespiti(round(parameters["lat"],1),round(float(ISS[1]),1),0.5) and
    yakinlik_tespiti(round(parameters["lng"],1),round(float(ISS[0]),1),0.5)):
        mesaj = "Uluslararasi Uzay Istasyonu su an itibariyle Bursa'nin ustunden " \
                "geciyor. Eger kodumuz dogruysa, hava karanlik ve yukarlarda bir " \
                "yerde istasyon var. Iyi Seyirler.."
        mail_at("CABUK HAVA BAK!!!",mesaj)
        print("mail atildi..")