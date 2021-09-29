from models import (Base, session, Product, engine)
import datetime
from datetime import datetime 
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


def view_product(user_input):
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    try:
        product_id = int(user_input)
    except ValueError:
        input ('''
        \n!!!!!! ID ERROR !!!!!!
        \r The Id should be in a number format
        \r Ex: 1 
        \r Press enter to return to menu and try again...
        \r!!!!!!!!!!!!!!!!!!!!!!
        ''')
        return 
    else:
        if product_id in id_options:
            chosen_product = session.query(Product).filter(Product.product_id==product_id).first()
            print(chosen_product)
            time.sleep(1.5)
            input('Press Enter to return to main menu....  ')
            return
        else:
            input(f'''
            \n!!!!!! ID ERROR !!!!!!
            \rThe ID you chose was unavailable.
            \rPlease review the following list and try again.
            \rOptions: {id_options}
            \rPress enter to return to menu and try again.....  ''')
            return 
            
def add_product():
    name = input ('What is the name of the product you would like to add?   ')
    quantity =input (f'what is the quantity of {name}?   ')
    price = int(input (f'What is the price of {name}?   '))
    date = datetime.date(datetime.now())
    date_string = date.strftime("%Y-%m-%d")
    new_product = Product(product_name=name, product_quantity=quantity, date_updated= date, product_price= price)
    print(new_product)
    if session.query(Product).filter(Product.product_name == new_product.product_name).count() > 0:
        existing_product = session.query(Product).filter(
            Product.product_name == new_product.product_name)
        existing_product.product_quantity = quantity
        existing_product.product_price = price
        existing_product.date_updated = date
        session.commit()
        return
    else:
        session.add(new_product)
        session.commit()
        print('!!! YOUR PRODUCT HAS BEEN ADDED !!!')
        return






def app():
    app_running = True
    while app_running:
        choice = master_menu()
        if choice == 'v':
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            print(f'{id_options}')
            product_selection = input ('\n\nWhat product would you like to view? please only search by product Id #...  ')
            view_product(product_selection)
        elif choice == 'a':
            add_product()
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
    
