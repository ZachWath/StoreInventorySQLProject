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


def app():
    app_running = True
    #v for viewing a single product in the database, if product doesnt exist , error should display
    #   propmt to try again 
    #a to add a new product , if this is a duplicate , the system overwrites the most recent data
    #b for backing up the database , writted to a new csv file , should contain a single header line with
    #   the proper fields 
    #all user entries should be validated (check agains an options list)






if __name__ == '__main__':
    Base.metadata.create_all (engine)
    add_csv()

    for product in session.query(Product):
        print(product)