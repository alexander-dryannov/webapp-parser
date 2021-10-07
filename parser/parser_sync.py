import os
import csv
import uuid
import glob
import tabula
import sqlite3
import requests
from bs4 import BeautifulSoup as bs

class Parser:
    def __init__(self) -> None:
        self.current_wd = os.getcwd()
        self.database_directory = "/".join(self.current_wd.split("/")[0:-1]) + "/react/backend/db"
        self.database_name = "price"
        self.p1 = {"Aerosib": []}
        self.p2 = {"Aerodar": []}
        self.p3 = {"Transcomavia": []}
        self.p4 = {"Artis": []}
        self.p5 = {"Mdcargo": []}

    """Работа с базой данных"""
    # Создание БД
    def database_creation(self):
        sqlite3.connect(f'{self.database_directory}/{self.database_name}.db').close()

    # Запись в БД
    def writing_data_to_database(self):
        data = [ self.p1, self.p2, self.p3, self.p4, self.p5]
        con = sqlite3.connect(glob.glob(f"{self.database_directory}/*.db")[-1])
        cur = con.cursor()
        for d in data:
            cur.execute(f'''CREATE TABLE {next(iter(d.keys()))} (id, departure, appointment, AK, cost)''')
            con.commit()
            for item in d[next(iter(d.keys()))]:
                cur.execute(f"INSERT INTO {next(iter(d.keys()))} VALUES (?, ?, ?, ?, ?)", (uuid.uuid4().hex, item[0], item[1], item[2], str(item[3])))
            con.commit()
        con.close()
    """END"""

    """Чистки и проверки"""
    # Завершение. Удаление старой БД и переименование новой
    def completion(self):
        os.chdir(self.database_directory)
        if len(glob.glob("*.db")) > 1:
            os.remove("price.db")
            os.rename("newprice.db", "price.db")
        else:
            pass

    # Очистка директории от мусора
    @staticmethod 
    def cleaning_directory():
        try:
            os.remove(glob.glob("*.pdf")[0])
            os.remove(glob.glob("*.csv")[0])
        except IndexError:
            pass

    # Проверка на существование БД
    def check_db(self):
        if len(glob.glob(f"{self.database_directory}/*.db")) == 1:
            self.database_name = "newprice"
            self.database_creation()
        else:
            self.database_name = "price"
            self.database_creation()
    
    # Создание директории для БД
    def create_directory(self):
        print(self.current_wd)
        try:
            os.mkdir(self.database_directory)
        except FileExistsError:
            pass
        
    
    @staticmethod
    def check_cost(AK):
        aw = 650   
        wg = 800  
        yak = 750 
        kl = 650  

        if AK in ["РГ", "ЯК", "КЛ"]:
            if AK == "РГ":
                return wg
            elif AK == "ЯК":
                return yak
            elif AK == "КЛ":
                return kl
        else:
            return aw
    """END"""
    
    """Получение данных"""
    # Скачивание файлов pdf
    @staticmethod
    def get_file(filename, url):
        with open(filename + ".pdf", "wb") as pdf:
            pdf.write(requests.get(url).content)

    # Получение страниц для парсинга
    @staticmethod
    def get_soup(url):
        return bs(requests.get(url).text, "lxml")
    """END"""
    
    """Парсеры"""
    def aerosib(self):
        departure = "Москва"
        self.get_file("aerosib", "http://www.aerosib.ru/tarif.pdf")
        tabula.convert_into(input_path="aerosib.pdf", output_path="aerosib.csv", output_format="csv", pages="all")
        with open("aerosib.csv", newline='') as csvfile:
            spreadsheet = csv.reader(csvfile)
            for row in spreadsheet:
                if len(row) == 2:
                    if len(row[1].split()) > 2:
                        try:
                            if int(row[1].split()[-2]) > 500:
                                appointment = row[0]
                                ak = row[1].split(" ")[1]
                                cost = row[1].split(" ")[2]
                                self.p1["Aerosib"].append([departure, appointment, ak, cost])
                        except:
                            pass
                elif len(row) == 9:
                    raw_ak = " ".join(row[-7:-4]).split()
                    aks = [a for a in raw_ak if a != ""]
                    ak = ", ".join(aks).strip()
                    cost = row[-3]
                    self.p1["Aerosib"].append([departure, appointment, ak, cost])
                elif len(row) == 10:
                    if row[1].replace(' ', ',').split(',')[0].isupper() != True and row[1] != '':
                        appointment = row[1]
                        raw_ak = " ".join(row[-7:-4]).split()
                        aks = [a for a in raw_ak if a != ""]
                        ak = ", ".join(aks).strip()
                        cost = row[-4]
                        self.p1["Aerosib"].append([departure, appointment, ak, cost])
                    else:
                        break
        self.cleaning_directory()

    def aerodar(self):
        departure = "Москва"
        appointment = ''
        ak = ''
        cost = ''
        self.get_file("aerodar", "http://www.aerodar.ru/public_images/price_russia.pdf")
        tabula.convert_into(input_path="aerodar.pdf", output_path="aerodar.csv", output_format="csv", pages="all")

        with open("aerodar.csv", newline='') as csvfile:
            spreadsheet = csv.reader(csvfile)
            for row in spreadsheet:
                try:
                    if len(row[2]) > 3:
                        continue
                except IndexError:
                    pass
                if len(row) >= 3 and row[0] != '' and row[1] != '':
                    raw_data = row[0].split(" ")
                    if len(raw_data) == 1:
                        appointment = raw_data[0]
                        try:
                            if len(row[1].split(" ")) < 3:
                                ak = row[1]
                            else:
                                ak = row[1].split(" ")[0]
                        except IndexError:
                            pass
                        cost = self.check_cost(ak)
                        self.p2["Aerodar"].append([departure, appointment, ak, cost])

                    elif len(row) == 5:
                        appointment = row[0]
                        ak = row[1]
                        cost = self.check_cost(ak)
                        self.p2["Aerodar"].append([departure, appointment, ak, cost])
                    elif len(row[0].split()) == 2:
                        appointment = row[0].split()[0]
                        ak = row[0].split()[1]
                        cost = self.check_cost(ak)
                        self.p2["Aerodar"].append([departure, appointment, ak, cost])
                    elif len(row[0].split()) > 2:
                        raw_appointment = row[0].split()[0:3]
                        appointment = " ".join(raw_appointment)
                        ak = row[0].split()[-1]
                        cost = self.check_cost(ak)
                        self.p2["Aerodar"].append([departure, appointment, ak, cost])
        self.cleaning_directory()

    def scraping_transcomavia(self):
        soup = self.get_soup("https://www.transcomavia.ru/content/aviaperevozki-gruzov/")
        trs = soup.find("tbody", {"class":"data"}).find_all("tr")
        for td in trs:
            d = td.text.replace(" ", "").split("\n")
            appointment = d[2]
            departure = d[3]
            ak = "-"
            cost = d[5]
            self.p3["Transcomavia"].append([departure, appointment, ak, cost])

    def scraping_artis(self):
        departure = "Москва"
        soup = self.get_soup("https://www.artis-logistics.ru/uslugi/aviaperevozki/iz-moskvy")
        trs = soup.find("tbody").find_all("tr")
        for td in trs:
            ak = "-"
            raw_appointment = td.text.split()
            if raw_appointment[0] != "#REF!" and td.text.split()[0] != "#N/A":
                if len(raw_appointment) == 5:
                    appointment = " ".join(raw_appointment[0:2])
                    cost = " ".join(td.text.split()[1:])
                    self.p4["Artis"].append([departure, appointment, ak, cost])
                elif len(raw_appointment) == 6:
                    appointment = " ".join(raw_appointment[0:-3])
                    cost = " ".join(td.text.split()[3:])
                    self.p4["Artis"].append([departure, appointment, ak, cost])
                else:
                    appointment = raw_appointment[0]
                    cost = " ".join(td.text.split()[1:])
                    self.p4["Artis"].append([departure, appointment, ak, cost])

    def scraping_md_cargo(self):
        soup = self.get_soup("https://www.md-cargo.ru/tariffs/tarify-na-aviaperevozki-po-rf/")
        trs = soup.find("tbody").find_all("tr")
        for td in trs:
            if len(td.text.split()) == 8:
                departure = td.text.split()[2]
                appointment = td.text.split()[0]
                ak = td.text.split()[1]
                cost = td.text.split()[-1]
                self.p5["Mdcargo"].append([departure, appointment, ak, cost])
            if len(td.text.split()) == 9:
                departure = td.text.split()[3]
                appointment = " ".join(td.text.split()[0:2])
                ak = td.text.split()[3]
                cost = td.text.split()[-1]
                self.p5["Mdcargo"].append([departure, appointment, ak, cost])
            if len(td.text.split()) == 10:
                departure = td.text.split()[4]
                appointment = " ".join(td.text.split()[0:3])
                ak = td.text.split()[3]
                cost = td.text.split()[-1]
                self.p5["Mdcargo"].append([departure, appointment, ak, cost])
    """END"""

if __name__ == "__main__":
    p = Parser()
    p.create_directory()
    p.cleaning_directory()
    p.check_db()
    p.scraping_transcomavia()
    p.scraping_artis()
    p.scraping_md_cargo()
    p.aerosib()
    p.aerodar()
    p.writing_data_to_database()
    p.completion()