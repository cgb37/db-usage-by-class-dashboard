import csv
import random
import requests
from faker import Faker
from flask import Flask
from io import StringIO

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'



@app.route('/fakerdata')
def fakerdata():
    csv_file = 'faker_data.csv'
    fake = Faker()

    # Generate random classification
    classifications = ['freshman', 'sophomore', 'junior', 'senior', 'graduate', 'doctorate', 'faculty']
    classification = random.choice(classifications)

    # Fetch list of databases from the URL
    databases_url = 'https://raw.githubusercontent.com/cgb37/db-usage-by-class-dashboard/main/subjectsplus5_dev_db_record.csv'
    response = requests.get(databases_url)
    databases = response.text.strip().split('\n')

    # Generate random database
    database = random.choice(databases)

    # Fetch list of majors from the URL
    majors_url = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/majors-list.csv'
    response = requests.get(majors_url)
    majors = response.text.strip().split('\n')

    # Generate random major
    major = random.choice(majors)

    # Generate random access location
    access_locations = ['on campus', 'off campus']
    access_location = random.choice(access_locations)

    # Create CSV data
    data = [[classification, database, major, access_location]]

    for _ in range(1000):
        classification = random.choice(classifications)
        database = random.choice(databases)
        major = random.choice(majors)
        access_locations = ['on campus', 'off campus']
        access_location = random.choice(access_locations)
        data.append([classification, database, major, access_location])

    # Write data to CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return f"CSV data has been generated and saved to '{csv_file}' successfully."

@app.route('/removequotes')
def remove_quotes():
    csv_file_url = 'https://raw.githubusercontent.com/cgb37/db-usage-by-class-dashboard/main/faker_data.csv'
    response = requests.get(csv_file_url)
    lines = response.text.strip().split('\n')

    data = []
    for line in lines:
        csv_reader = csv.reader(StringIO(line), delimiter=',', quotechar='"')
        for row in csv_reader:
            if len(row) >= 2:
                database = row[1].strip()
                if database.startswith('"') and database.endswith('"'):
                    row[1] = database[1:-1]
            data.append(row)

    # Write data to a new CSV file without quotes
    csv_file = 'noquotes.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return f"Quotes removed from 'database' column. Data saved to '{csv_file}' successfully."


def strip_before_second_comma(string):
    split_string = string.split(',', maxsplit=2)
    if len(split_string) >= 3:
        value = split_string[2]
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1].strip()
        return value.strip()
    return string

@app.route('/cleandata')
def clean_data():
    csv_file_url = 'https://raw.githubusercontent.com/cgb37/db-usage-by-class-dashboard/main/faker_data.csv'
    response = requests.get(csv_file_url)
    lines = response.text.strip().split('\n')

    cleaned_data = []
    for line in lines:
        row = line.split(',')
        if len(row) >= 3:
            cleaned_data.append([strip_before_second_comma(row[2])])

    # Write data to a new CSV file
    csv_file = 'cleaned_data.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(cleaned_data)

    return f"Cleaned data has been saved to '{csv_file}' successfully."

if __name__ == '__main__':
    app.run(debug=True)
