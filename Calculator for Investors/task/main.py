import csv
import os
import sqlite3

from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, Session, query
from sqlalchemy import Column, Float, String



data_config = ["companies", "financial"]
sql_file = "investor.db"


menu_dict = {"MAIN MENU": ["Exit", "CRUD operations", "Show top ten companies by criteria"],
             "CRUD MENU": ["Back", "Create a company", "Read a company", "Update a company", "Delete a company", "List all companies"],
             "TOP TEN MENU": ["Back", "List by ND/EBITDA", "List by ROE", "List by ROA"]}

new_company_dict = {"ticker": ["Enter ticker (in the format 'MOON'):", ""],
                    "name": ["Enter company (in the format 'Moon Corp'):", ""],
                    "industry": ["Enter industries (in the format 'Technology'):", ""],
                    "ebitda": ["Enter ebitda (in the format '987654321'):", 0],
                    "sales": ["Enter sales (in the format '987654321'):", 0],
                    "net_prof": ["Enter net profit (in the format '987654321'):", 0],
                    "market_prc": ["Enter market price (in the format '987654321'):", 0],
                    "net_debt": ["Enter net debt (in the format '987654321'):", 0],
                    "assets": ["Enter assets (in the format '987654321'):", 0],
                    "equity": ["Enter equity (in the format '987654321'):", 0],
                    "cash_eq": ["Enter cash equivalents (in the format '987654321'):", 0],
                    "liabil": ["Enter liabilities (in the format '987654321'):", 0]}

base = declarative_base()


class Companies(base):
    __tablename__ = 'companies'

    ticker = Column(String(10), primary_key=True)
    name = Column(String(50))
    sector = Column(String(50))


class Financial(base):
    __tablename__ = 'financial'

    ticker = Column(String(10), primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


class CfiProgram():
    menu_level = 0
    menu_selected = 0

    def ask_and_check(self, maxmenu_num):
        selected_item = -1
        print("Enter an option:")
        try:
            selected_item = int(input())
            if selected_item > maxmenu_num:
                selected_item = -1
                print("Invalid option!")
        except:
                print("Invalid option!")
        return selected_item


    def print_company_list(self, company_name):
        sql_query = f"SELECT * FROM 'companies' WHERE name like '%{company_name}%';"
        self.curs.execute(sql_query)
        self.sqlconn.commit()

        # print("Q - >",self.curs.rowcount, sql_query)
        company_dict = {}
        result = self.curs.fetchall()
        if result:
            for num, row in enumerate(result):
                company_dict[num] = [row['ticker'], row['name']]
                print(num, row['name'])

            print("Enter company number:")
            sel_company = int(input())
            return sel_company, company_dict
        else:
            print("Company not found!")
            return -1, {}


    def edit_company(self, cedit=0, company_name=None):

        # company exist and we should edit it
        if company_name and cedit == 0:
            # # here we should find company
            sel_company, company_dict = self.print_company_list(company_name)

            if sel_company >= 0:
                sql_query = f"SELECT * FROM 'financial' WHERE ticker = '{company_dict[sel_company][0]}';"
                self.curs.execute(sql_query)
                self.sqlconn.commit()
                elem = self.curs.fetchone()

                print(company_dict[sel_company][0], company_dict[sel_company][1])
                print("P/E =", round(elem['market_price'] / elem['net_profit'], 2))
                print("P/S =", round(elem['market_price'] / elem['sales'], 2))
                print("P/B =", round(elem['market_price'] / elem['assets'], 2))
                if elem['ebitda'] == None:
                    nd_ebitda = None
                else:
                    nd_ebitda = round(elem['net_debt'] / elem['ebitda'], 2)
                print("ND/EBITDA =", nd_ebitda)
                print("ROE =", round(elem['net_profit'] / elem['equity'], 2))
                print("ROA =", round(elem['net_profit'] / elem['assets'], 2))
                print("L/A =", round(elem['liabilities'] / elem['assets'], 2))

        else:
            if cedit == 0 or cedit == 1:
                pass_count = 0
                if cedit == 1:
                    sel_company, company_dict = self.print_company_list(company_name)
                    pass_count = 3

                for key, m_elem in new_company_dict.items():
                    if pass_count > 0:
                        pass_count -= 1
                        continue
                    print(m_elem[0])
                    if type(m_elem[1]) == str:
                        new_company_dict[key][1] = input()
                    else:
                        new_company_dict[key][1] = int(input())


                if cedit == 0:
                    sql_query = "INSERT INTO 'companies' VALUES(?, ?, ?);"
                    self.curs.execute(sql_query, (new_company_dict['ticker'][1],
                                                  new_company_dict['name'][1],
                                                  new_company_dict['industry'][1]))


                    sql_query = "INSERT INTO 'financial' VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
                    self.curs.execute(sql_query, (new_company_dict['ticker'][1],
                                                  new_company_dict['ebitda'][1],
                                                  new_company_dict['sales'][1],
                                                  new_company_dict['net_prof'][1],
                                                  new_company_dict['market_prc'][1],
                                                  new_company_dict['net_debt'][1],
                                                  new_company_dict['assets'][1],
                                                  new_company_dict['equity'][1],
                                                  new_company_dict['cash_eq'][1],
                                                  new_company_dict['liabil'][1]
                                                  ))
                    self.sqlconn.commit()
                    print("Company created successfully!")
                else:

                    sql_query = "UPDATE 'financial' SET ebitda=?, sales=?, net_profit=?, market_price=?," \
                                "net_debt=?, assets=?, equity=?, cash_equivalents=?, liabilities=? WHERE ticker=?;"
                    self.curs.execute(sql_query, (new_company_dict['ebitda'][1],
                                                  new_company_dict['sales'][1],
                                                  new_company_dict['net_prof'][1],
                                                  new_company_dict['market_prc'][1],
                                                  new_company_dict['net_debt'][1],
                                                  new_company_dict['assets'][1],
                                                  new_company_dict['equity'][1],
                                                  new_company_dict['cash_eq'][1],
                                                  new_company_dict['liabil'][1],
                                                  company_dict[sel_company][0]))
                    self.sqlconn.commit()
                    print("Company updated successfully!")
            elif cedit == 100:

                sel_company, company_dict = self.print_company_list(company_name)

                if sel_company > -1 and company_dict != {}:
                    sql_query = "DELETE FROM 'financial' WHERE ticker=?;"
                    self.curs.execute(sql_query, (company_dict[sel_company][0],))

                    sql_query = "DELETE FROM 'companies' WHERE ticker=?;"
                    self.curs.execute(sql_query, (company_dict[sel_company][0],))
                    self.sqlconn.commit()
                    print("Company deleted successfully!")


    def show_comp_list(self):
        sql_query = f"SELECT * FROM 'companies' ORDER BY ticker;"
        self.curs.execute(sql_query)
        self.sqlconn.commit()

        print("COMPANY LIST")
        result = self.curs.fetchall()
        if result:
            for row in result:
                print(row[0], row[1], row[2])

    def __init__(self):
        with sqlite3.connect(f"C:\\Users\\KoliaS-PC\\PycharmProjects\\Calculator for Investors\\Calculator for Investors\\task\\{sql_file}") as sqlite_conn:
            self.sqlconn = sqlite_conn
            sqlite_conn.row_factory = sqlite3.Row
            self.curs = sqlite_conn.cursor()

            print("Welcome to the Investor Program!")
            print()

            while True:
                menu_key = list(menu_dict.keys())[self.menu_selected]
                menu_list = menu_dict[menu_key]
                print(menu_key)  # Print menu header



                # print menu items
                for number, name in enumerate(menu_list):
                    print(number, name)

                # user prompt
                user_input = self.ask_and_check(len(menu_list))

                # user prompt actions
                if user_input == 0:
                    if self.menu_level == 0:
                        print("Have a nice day!")
                        self.menu_level = -1
                        break
                    else:
                        self.menu_level = 0
                        self.menu_selected = 0

                if user_input > 0 and self.menu_level == 1:
                    if menu_key != "TOP TEN MENU":
                        if user_input == 1:
                            self.edit_company(0)
                        elif user_input == 2:
                            print("Enter company name:")
                            u_company_name = str(input())
                            if u_company_name:
                                self.edit_company(0, u_company_name)
                            # print()
                        elif user_input == 3:
                            print("Enter company name:")
                            u_company_name = str(input())
                            if u_company_name:
                                self.edit_company(1, u_company_name)
                        elif user_input == 4:
                            print("Enter company name:")
                            u_company_name = str(input())
                            if u_company_name:
                                self.edit_company(100, u_company_name)
                        elif user_input == 5:
                            self.show_comp_list()

                        self.menu_level = 0
                        self.menu_selected = 0
                        # print()
                    else:
                        print("Not implemented!")
                        self.menu_level = 0
                        self.menu_selected = 0
                        print()

                elif user_input > -1:
                    if self.menu_level == 0:
                        self.menu_selected = user_input
                        self.menu_level = 1



def etl_data():

    # if os.path.exists(sql_file):
    #     os.remove(sql_file)

    engine = create_engine(f'sqlite:///C:\\Users\\KoliaS-PC\\PycharmProjects\\Calculator for Investors\\Calculator for Investors\\task\\{sql_file}', echo=True)
    base.metadata.create_all(engine)

    with Session(engine) as session:
        for data_id, data_name in enumerate(data_config):
            with open(f"{data_name}.csv") as csv_pf:
                comp = list(csv.DictReader(csv_pf))
                for elem in comp:
                    print(elem)
                    if data_id == 0:
                        session.add(Companies(**elem))
                    elif data_id == 1:
                        for key in elem.keys():
                            if elem[key] == '':
                                elem[key] = None

                        session.add(Financial(**elem))
            session.commit()
    if os.path.exists(sql_file) and os.path.getsize(sql_file) == 36864:
        print("Database created successfully!")


# etl_data()
CfiProgram()