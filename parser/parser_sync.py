import os
import csv
import uuid
import glob
import tabula
import sqlite3
import requests
from multiprocessing import Process
from bs4 import BeautifulSoup as bs

# Переменные
current_wd = os.getcwd()
database_directory = "/".join(current_wd.split("/")[0:-1]) + "/db"
database_name = ""

# Завершение. Удаление старой БД и переименование новой
def completion():
    os.chdir(database_directory)
    if len(glob.glob("*.db")) > 1:
        pass
        os.remove("price.db")
        os.rename("new_price.db", "price.db")
    else:
        pass

# Очистка директории от мусора 
def cleaning_directory():
    try:
        os.remove(glob.glob("*.pdf")[0])
        os.remove(glob.glob("*.csv")[0])
    except IndexError:
        pass

# Создание БД
def database_creation():
    global database_name
    sqlite3.connect(f'{database_directory}/{database_name}.db').close()

# Создание таблиц
def create_table(table_name):
    global database_name
    con = sqlite3.connect(f"{database_directory}/{database_name}.db")
    cur = con.cursor()
    cur.execute(f'''CREATE TABLE {table_name} (id, departure, appointment, AK, cost)''')
    con.commit()
    con.close()

# Проверка на существование БД
def check_db():
    global database_name
    if len(glob.glob(f"{database_directory}/*.db")) == 1:
        database_name = "new_price"
        database_creation()
    else:
        database_name = "price"
        database_creation()

# Скачивание файлов pdf
def get_file(url):
    with open(url.split("/")[-1], "wb") as pdf:
        pdf.write(requests.get(url).content)

# Получение страниц для парсинга
def get_soup(url):
    return bs(requests.get(url).text, "lxml")

# Запись в БД
def writing_data_to_database(table_name, departure, appointment, ak, cost):
    # print(table_name, departure, appointment, ak, cost)
    id = uuid.uuid4().hex
    con = sqlite3.connect(glob.glob(f"{database_directory}/*.db")[0])
    cur = con.cursor()
    cur.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?)", (id, departure, appointment, ak, str(cost)))
    con.commit()
    con.close()

def aerosib():
    table_name = "Aerosib"
    departure = "Москва"
    get_file("http://www.aerosib.ru/tarif.pdf")
    create_table(table_name)
    tabula.convert_into(input_path=glob.glob(f"{current_wd}/*.pdf")[0], output_path=f"{current_wd}/aerosib.csv", output_format="csv", pages="all")
    with open(glob.glob(f"{current_wd}/*.csv")[0], newline='') as csvfile:
        spreadsheet = csv.reader(csvfile)
        for row in spreadsheet:
            if len(row) == 2:
                if len(row[1].split()) > 2:
                    try:
                        if int(row[1].split()[-2]) > 500:
                            appointment = row[0]
                            ak = row[1].split(" ")[1]
                            cost = row[1].split(" ")[2]
                            writing_data_to_database(table_name, departure, appointment, ak, cost)
                    except:
                        pass
            elif len(row) == 9:
                raw_ak = " ".join(row[-7:-4]).split()
                aks = [a for a in raw_ak if a != ""]
                ak = ", ".join(aks).strip()
                cost = row[-3]
                writing_data_to_database(table_name, departure, appointment, ak, cost)
            elif len(row) == 10:
                if row[1].replace(' ', ',').split(',')[0].isupper() != True and row[1] != '':
                    appointment = row[1]
                    raw_ak = " ".join(row[-7:-4]).split()
                    aks = [a for a in raw_ak if a != ""]
                    ak = ", ".join(aks).strip()
                    cost = row[-4]
                    writing_data_to_database(table_name, departure, appointment, ak, cost)
                else:
                    break
    cleaning_directory()

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

def aerodar():
    departure = "Москва"
    appointment = ''
    ak = ''
    cost = ''
    table_name = "Aerodar"
    get_file("http://www.aerodar.ru/public_images/price_russia.pdf")
    create_table(table_name)
    tabula.convert_into(input_path=glob.glob(f"{current_wd}/*.pdf")[0], output_path=f"{current_wd}/aerodar.csv", output_format="csv", pages="all")

    with open(glob.glob(f"{current_wd}/*.csv")[0], newline='') as csvfile:
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
                    cost = check_cost(ak)
                    writing_data_to_database(table_name, departure, appointment, ak, cost)

                elif len(row) == 5:
                    appointment = row[0]
                    ak = row[1]
                    cost = check_cost(ak)
                    writing_data_to_database(table_name, departure, appointment, ak, cost)
                elif len(row[0].split()) == 2:
                    appointment = row[0].split()[0]
                    ak = row[0].split()[1]
                    cost = check_cost(ak)
                    writing_data_to_database(table_name, departure, appointment, ak, cost)
                elif len(row[0].split()) > 2:
                    raw_appointment = row[0].split()[0:3]
                    appointment = " ".join(raw_appointment)
                    ak = row[0].split()[-1]
                    cost = check_cost(ak)
                    writing_data_to_database(table_name, departure, appointment, ak, cost)
    cleaning_directory()

def scraping_transcomavia():
    table_name = "Transcomavia"
    create_table(table_name)
    soup = get_soup("https://www.transcomavia.ru/content/aviaperevozki-gruzov/")
    trs = soup.find("tbody", {"class":"data"}).find_all("tr")
    for td in trs:
        d = td.text.replace(" ", "").split("\n")
        appointment = d[2]
        departure = d[3]
        ak = "-"
        cost = d[5]
        writing_data_to_database(table_name, departure, appointment, ak, cost)

def scraping_artis():
    table_name = "Artis"
    departure = "Москва"
    create_table(table_name)
    soup = get_soup("https://www.artis-logistics.ru/uslugi/aviaperevozki/iz-moskvy")
    trs = soup.find("tbody").find_all("tr")
    for td in trs:
        ak = "-"
        raw_appointment = td.text.split()
        if raw_appointment[0] != "#REF!" and td.text.split()[0] != "#N/A":
            if len(raw_appointment) == 5:
                appointment = " ".join(raw_appointment[0:2])
                cost = " ".join(td.text.split()[1:])
                writing_data_to_database(table_name, departure, appointment, ak, cost)
            elif len(raw_appointment) == 6:
                appointment = " ".join(raw_appointment[0:-3])
                cost = " ".join(td.text.split()[3:])
                writing_data_to_database(table_name, departure, appointment, ak, cost)
            else:
                appointment = raw_appointment[0]
                cost = " ".join(td.text.split()[1:])
                writing_data_to_database(table_name, departure, appointment, ak, cost)

def scraping_md_cargo():
    table_name = "Mdcargo"
    create_table(table_name)
    soup = get_soup("https://www.md-cargo.ru/tariffs/tarify-na-aviaperevozki-po-rf/")
    trs = soup.find("tbody").find_all("tr")
    for td in trs:
        if len(td.text.split()) == 8:
            departure = td.text.split()[2]
            appointment = td.text.split()[0]
            ak = td.text.split()[1]
            cost = td.text.split()[-1]
            writing_data_to_database(table_name, departure, appointment, ak, cost)
        if len(td.text.split()) == 9:
            departure = td.text.split()[3]
            appointment = " ".join(td.text.split()[0:2])
            ak = td.text.split()[3]
            cost = td.text.split()[-1]
            writing_data_to_database(table_name, departure, appointment, ak, cost)
        if len(td.text.split()) == 10:
            departure = td.text.split()[4]
            appointment = " ".join(td.text.split()[0:3])
            ak = td.text.split()[3]
            cost = td.text.split()[-1]
            writing_data_to_database(table_name, departure, appointment, ak, cost)

if __name__ == "__main__":
    cleaning_directory()
    check_db()
    scraping_transcomavia()
    scraping_artis()
    scraping_md_cargo()
    aerosib()
    aerodar()
    completion()