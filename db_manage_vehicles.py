#!venv/bin/python3

from app import db
from app.models import Vehicle
import getpass
import os


def add_vehicle():
    os.system('clear')
    name = input('Vehicle name: ')
    password = getpass.getpass('Password: ')
    mileage = input('Mileage: ')
    v = Vehicle(name=name, password=password, total_mileage=mileage)
    db.session.add(v)
    db.session.commit()


def delete_vehicle():
    error = []
    while True:
        os.system('clear')
        if error:
            print('\n'.join(error))
            error = []
        vehicles = Vehicle.query.all()
        for v in vehicles:
            print('{}: {}'.format(v.id, v.name))
        id = input('Vehicle # to delete: ')
        password = getpass.getpass('Password: ')
        try:
            id = int(id)
        except ValueError:
            error.append('Enter a valid vehicle number')
        v = Vehicle.query.get(id)
        if v and v.verify_password(password):
            print('Password Verified')
            break
        else:
            error.append('Invalid password')
    db.session.delete(v)
    db.session.commit()


def main():
    choice = 1
    while True:
        os.system('clear')
        print('1: Add vehicle')
        print('2: Delete vehicle')
        try:
            choice = int(input())
            break
        except ValueError:
            pass
    if choice == 1:
        add_vehicle()
    elif choice == 2:
        delete_vehicle()
    for v in Vehicle.query.all():
        print(v)

if __name__ == '__main__':
    main()