import urllib.request
import csv
import pymongo
import requests
import os

MONGODB_K8S_SVC = os.getenv("MONGODB_K8S_SVC", "mongodb")
MONGODB_K8S_SVC_PORT = os.getenv("MONGODB_K8S_SVC_PORT", 27017)
MONGODB_URI = f"mongodb://{MONGODB_K8S_SVC}:{MONGODB_K8S_SVC_PORT}"

DATABASE_NAME = os.getenv("DATABASE_NAME", "openflights")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "airports")
DATA_URL = os.getenv("DATA_URL", "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports-extended.dat")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH", "")

SERVER_K8S_SVC = os.getenv("SERVER_K8S_SVC", "myServer")
SERVER_K8S_SVC_PORT = os.getenv("SERVER_K8S_SVC_PORT", 5050)
SERVER_URL = f"http://{SERVER_K8S_SVC}:{SERVER_K8S_SVC_PORT}/posts"


def create_post(author, title, tags, body):
    data = {
        "author": author,
        "title": title,
        "tags": tags.split(","),  # Split tags into an array
        "body": body
    }

    response = requests.post(SERVER_URL, json=data, headers={"content-type": "application/json"})

    if response.status_code == 201 or response.status_code == 200:  # 201 is for successful creation
        print("\nPost created successfully:", response.json())
    else:
        print("Failed to create post", response.status_code, response.text)


def list_posts_and_save_to_csv():
    response = requests.get(SERVER_URL)

    if response.status_code == 200:
        posts = response.json()
        print(posts)

        with open(f"{CSV_FILE_PATH}/posts.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Title", "Body", "Author", "Tags"])
            for post in posts:
                writer.writerow([post.get("id"), post.get("title"), post.get("body"), post.get("author"), post.get("tags", [])])

        print("Posts saved to posts.csv")
    else:
        print("Failed to retrieve posts", response.status_code, response.text)


def import_data_to_db():
    client = pymongo.MongoClient(MONGODB_URI)
    db_list = client.list_database_names()
    if DATABASE_NAME in db_list:
        print("Data already imported.")
        return

    print("Downloading data...")
    urllib.request.urlretrieve(DATA_URL, "airports-extended.dat")
    print("Download complete")

    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    with open("airports-extended.dat", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            document = {
                "Airport ID": row[0],
                "Name": row[1],
                "City": row[2],
                "Country": row[3],
                "IATA": row[4],
                "ICAO": row[5],
                "Latitude": row[6],
                "Longitude": row[7],
                "Altitude": row[8],
                "Timezone": row[9],
                "DST": row[10],
                "Tz database time zone": row[11],
                "Type": row[12],
                "Source": row[13]
            }
            collection.insert_one(document)
    print("Data imported successfully.")


def export_data_to_csv():
    if os.path.exists(f"{CSV_FILE_PATH}/airports_data.csv"):
        print(f"File airports_data.csv already exists. Skipping export.")
        return

    client = pymongo.MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    cursor = collection.find()

    with open(f"{CSV_FILE_PATH}/airports_data.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz Database Time Zone", "Type", "Source"])

        for document in cursor:
            writer.writerow([
                document.get("Airport ID"),
                document.get("Name"),
                document.get("City"),
                document.get("Country"),
                document.get("IATA"),
                document.get("ICAO"),
                document.get("Latitude"),
                document.get("Longitude"),
                document.get("Altitude"),
                document.get("Timezone"),
                document.get("DST"),
                document.get("Tz database time zone"),
                document.get("Type"),
                document.get("Source")
            ])

    print("Data exported successfully to airports_data.csv.")


if __name__ == "__main__":
    import_data_to_db()
    export_data_to_csv()

    author_input = "John Doe"
    title_input = "Learning Python APIs"
    tags_input = "python,api,requests"
    body_input = "This is a body of the post to test API post requests."
    create_post(author_input, title_input, tags_input, body_input)

    list_posts_and_save_to_csv()
    exit(0)
