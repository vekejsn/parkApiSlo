import csv

def csv_to_obj(csv_content):
    # Convert the CSV content into a list of dictionaries
    reader = csv.DictReader(csv_content.splitlines(), delimiter=";")
    return [row for row in reader]

if __name__ == "__main__":
    print(csv_to_obj("name,age\nJohn,25\nJane,24\n"))  # [{'name': 'John', 'age': '25'}, {'name': 'Jane', 'age': '24'}]