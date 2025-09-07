import pandas as pd
from sqlite3 import connect,Error
from scrap import scrap
import os


base_path = os.path.dirname(__file__)  # Folder where database.py is located
db_path = os.path.join(base_path, "products.db")


def create_db():
    product_data = scrap()

    df = pd.DataFrame(product_data)
    try:
        conn = connect(database=db_path)
        mycursor = conn.cursor()
        table_creation_command = """Create Table if not exists T_products( 
                                    id Integer PRIMARY KEY AUTOINCREMENT,
                                    name  Varchar(50), 
                                    quantity Varchar(20),
                                    brand Varchar(40),
                                    categories Varchar(120),
                                    countries Varchar(30),
                                    nutrition_grade Varchar(10),
                                    energy_per_serving Varchar(10),
                                    fat_per_serving Varchar(10),                             
                                    carbohydrates_per_serving Varchar(10),
                                    protein_per_serving Varchar(10)  
                                                                )"""
        mycursor.execute(table_creation_command)
        conn.commit()
        print("Everything worked just fine database and the table were created and the fields were inserted into the database")

    except Error as error: 
        print("sqlite error :" , error)

    df.to_sql("T_products" , conn , if_exists= "replace" , index=False) 
    df.to_csv("newcsv3.csv" , index=False)  



def search_products(brand = None, country = None):   
    query = "select DISTINCT name , brand , energy_per_serving, countries from T_products where 1=1 "
    params = []
    if brand:
        query += " and brand like ?"
        params.append(f"%{brand}%")
    
    if country:
        query += " and countries like ?"
        params.append(f"%{country}%")

    conn = connect(database=db_path)  
    mycursor = conn.cursor()
    mycursor.execute(query , params)
    results = mycursor.fetchall()
    conn.close()
    return results



def get_all_brands():
    conn = connect(database= db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT brand FROM T_products WHERE brand IS NOT NULL AND brand != ''")
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]


def get_all_countries():
    conn = connect(database = db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT countries FROM T_products WHERE countries IS NOT NULL AND countries != ''")
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]

    





