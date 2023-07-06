import csv
import random
import requests
from faker import Faker
from flask import Flask

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



if __name__ == '__main__':
    app.run(debug=True)
