from models import (Base, session, Product, engine)
import datetime
import csv
import time

def clean_price(price_str):
    split_price_str = price_str.replace('$','')
    price_float = float(split_price_str)
    return int(price_float * 100)



def clean_date(date_str):
    split_date = date_str.split('/')
    month = int(split_date[0])
    day = int(split_date[1])
    year = int(split_date[2])
    return_date = datetime.date(year, month, day)
    return return_date



def add_csv():
    with open ('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_already_added = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_already_added == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = int(row[2])
                product_date = clean_date(row[3])
                new_product = Product(product_name=product_name, product_price=product_price,
                                        product_quantity=product_quantity, date_updated=product_date)
                session.add(new_product)
        session.commit()


def master_menu():
    while True:
        print('''
            ***************WELCOME TO THE STORE INVENTORY MENU***************
            \nPlease choose from the following options ..... 
            \r
            \rOPTIONS:
            \rTo view a product's info in the inventory, press "v"...
            \rTo add a new product to the inventory, press "a"...
            \rTo create a backup of the current inventory database, press "b"...
            \r ''')
        possible_answers = ['v', 'a', 'b']
        answer = input('What option would you like to do?...   ')
        if answer.lower() in possible_answers:
            return answer
        else:
            input('''That is not a valid option, please choose from the list provided...
            \n Press ENTER to continue....''')
def app():
    app_running = True
    while app_running:
        choice = master_menu()
        if choice == 'v':
            pass
    #v for viewing a single product in the database, if product doesnt exist , error should display
    #   propmt to try again
        elif choice == 'a':
    #a to add a new product , if this is a duplicate , the system overwrites the most recent data
            pass

        elif choice == 'b':
    #b for backing up the database , writted to a new csv file , should contain a single header line with
    #   the proper fields 
            pass
        else:
            app_running = False
    #all user entries should be validated (check agains an options list)






if __name__ == '__main__':
    Base.metadata.create_all (engine)
    add_csv()
    app()
    