import csv


def write_csv(input_person:list):
    with open('person.csv', 'w', encoding='utf8') as file:
        fields = ['name', 'age', 'job']
        writer = csv.DictWriter(file, fields, delimiter=';')
        writer.writeheader()

        for user in input_person:
            writer.writerow(user)

    
if __name__ == "__main__":
    persons = [
        {'name': 'Маша', 'age': 25, 'job': 'Scientist'}, 
        {'name': 'Вася', 'age': 8, 'job': 'Programmer'}, 
        {'name': 'Эдуард', 'age': 48, 'job': 'Big boss'},
    ]
    write_csv(persons)