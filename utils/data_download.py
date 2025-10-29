import os
import mysql.connector
import csv
from dotenv import load_dotenv
from datetime import datetime


def get_newest(path):
    """
    Finds the newest file in the given path.
    :param path: Path to the directory to find the newest file.
    :return newest_date: The date of the newest file.
    """
    # traverse the given path
    try:
        all_files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    except FileNotFoundError:
        print(f"No such directory: {path}")
        return None
    except PermissionError:
        print(f"Cannot access the directory: {path}")
        return None

    newest_date = None

    for file in all_files:
        file_name = file.split(".")[0]
        file_date = datetime.strptime(file_name, '%Y-%m-%d-%H-%M-%S')
        if newest_date is None or newest_date < file_date:
            newest_date = file_date

    if newest_date is not None:
        return newest_date
    else:
        print(f"No stored dataset yet in path: {path}")
        return None


def get_data(path):
    """
    Gets the dataset from the given path.
    If there is dataset in the path, then gets the newly added dataset.
    :param path: Path to store the dataset
    :return None
    """
    # connect the database
    # load the .env
    load_dotenv()
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )
    except mysql.connector.Error as err:
        print(err)
        return

    cursor = conn.cursor()

    # get the last newest fetch file date
    newest_date = get_newest(path)
    if newest_date is None:
        print(f"No stored dataset yet!")
        print(f"Fetching all dataset from database!")
        sql = "SELECT content, parse_content FROM cp_content"
        cursor.execute(sql)
    else:
        print(f"Last fetched dataset from database at {newest_date}!")
        print(f"Only updated dataset will be fetched from database!")
        sql = f"SELECT content, parse_content FROM cp_content WHERE time > %s"
        cursor.execute(sql, (newest_date,))

    # execute the query
    results = cursor.fetchall()
    if not results:
        print(f"No updated dataset available in database!")
        return
    # TODO: process the result

    # generate the filename
    filename = path + f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.csv'

    # write into .csv
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(i[0] for i in cursor.description)
        writer.writerows(results)

    # close connections
    cursor.close()
    conn.close()


if __name__ == '__main__':
    get_data('../datas/')
