import sys
from faker import Faker

try:
    file_name = sys.argv[1]
    file_format = sys.argv[2]
    num_rows = int(sys.argv[3])
except Exception:
    print("[!] Usage:\npython3 file_name file_format number_of_rows")
    pass

if not file_format in ("csv","json","txt","sqlite"):
    print("[!] Invaild Format -> {}".format(file_format))

fileds = ["first_name","last_name","country","address","birth"]


def get_data():
    try:
        faker = Faker()
        fname = faker.first_name()
        lname = faker.last_name()
        country = faker.country()
        address = faker.address()
        birth = str(faker.date_of_birth(minimum_age=18,maximum_age=70))
        data = {"first_name":fname,"last_name":lname,"country":country,"address":address,"birth":birth}
        return data
    
    except Exception as e:
        print("[!] Error: ", e)

with open(file_name,"w") as f_file:

    if file_format == "csv":
        import csv
        writer = csv.DictWriter(f_file,fieldnames=fileds)
        writer.writeheader()
        for _ in range(num_rows):
            data = get_data()
            writer.writerow(data)

    elif file_format == "json":
        import json
        json_data = []
        for _ in range(num_rows):
            data = get_data()
            json_data.append(data)

        json.dump(json_data,f_file,indent=4)

    elif file_format == "txt":
        for _ in range(num_rows):
            data = get_data()
            n = 0
            for key,value in data.items():
                    f_file.write("{}: {}\n".format(key,value))
                    n += 1

                    if n == 5:
                        f_file.write("\n")
                        n = 0

    elif file_format == "sqlite":
        import sqlite3

        create_tables = (
            """CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                country TEXT,
                address TEXT,
                birth DATE
            );""")

        with sqlite3.connect(file_name) as db:
            cursor = db.cursor()
            cursor.execute(create_tables)
            for _ in range(num_rows):
                data = get_data()
                cursor.execute("""
                    INSERT INTO users (first_name, last_name, country, address, birth)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    data.get("first_name"),
                    data.get("last_name"),
                    data.get("country"),
                    data.get("address"),
                    data.get("birth")
                ))
            db.commit()
