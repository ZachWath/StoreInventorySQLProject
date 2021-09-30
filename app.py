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


def clean_quantity(qty_input):
    bad_input = True
    qty_str = qty_input
    while bad_input:
        try:
            quantity_int = int(qty_str)
            bad_input = False
        except ValueError:
            print('''That quantity is not valid , plesae choose a whole number....
            \nExamples = 1 , 2, 3, etc...''')
            qty_str = input('What quantity would you like to choose?   ')
    return quantity_int


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
            else:
                if product_already_added.date_updated < clean_date(row[3]):
                    product_already_added.product_price = clean_price(row[1])
                    product_already_added.product_quantity = int(row[2])
                    product_already_added.date_updated = clean_date(row[3])
                else:
                    pass
        session.commit() 


def add_product():
    name = input('What is the name of the product you would like to add?   ')
    quantity = clean_quantity(input(f'what is the quantity of {name}?   '))
    price = clean_price((input(f'What is the price of {name}?   ')))
    current_date = datetime.date.today()
    new_product = Product(product_name=name, product_quantity=quantity,
                        date_updated=current_date, product_price=price)
    if session.query(Product).filter(Product.product_name == new_product.product_name).count() > 0:
        existing_product = session.query(Product).filter(
            Product.product_name == new_product.product_name).first()
        existing_product.product_quantity = new_product.product_quantity
        existing_product.product_price = new_product.product_price
        existing_product.date_updated = new_product.date_updated
        session.commit()
        return
    else:
        session.add(new_product)
        session.commit()
        print('!!! YOUR PRODUCT HAS BEEN ADDED !!!')
        return


def view_product(user_input):
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    try:
        product_id = int(user_input)
    except ValueError:
        input('''
        \n!!!!!! ID ERROR !!!!!!
        \r The Id should be in a number format
        \r Ex: 1 
        \r Press enter to return to menu and try again...
        \r!!!!!!!!!!!!!!!!!!!!!!
        ''')
        return
    else:
        if product_id in id_options:
            chosen_product = session.query(Product).filter(
                Product.product_id == product_id).first()
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


def backup():
    with open('inventory_backup.csv', 'w', newline='') as backup_file:
        data_list = []
        for product in session.query(Product):
            data_list.append(
                [product.product_name, f'${product.product_price/100}', product.product_quantity, product.date_updated])
        writer = csv.writer(backup_file)
        writer.writerow(['product_name', 'product_price',
                        'product_quantity', 'date_updated'])
        for product in data_list:
            writer.writerow(product)
        return


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
            \rTo EXIT the program, press "e"...  ''')
        possible_answers = ['v', 'a', 'b','e']
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
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            print("\nThese are the available options...")
            print(f'\n{id_options}')
            product_selection = input ('\n\nWhat product would you like to view? please only search by product Id #...  ')
            view_product(product_selection)
        elif choice == 'a':
            add_product()
            pass
        elif choice == 'b':
            backup()
            pass
        elif choice == 'e':
            print ("\nThank you for using this progam!")
            print ("\nThe program will close in...")
            time.sleep(1.25)
            print("3...")
            time.sleep(1.25)
            print("2...")
            time.sleep(1.25)
            print("1...")
            time.sleep(1.25)
            print("NOW")
            app_running = False



if __name__ == '__main__':
    Base.metadata.create_all (engine)
    add_csv()
    app()
    
