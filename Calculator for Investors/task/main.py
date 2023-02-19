

# menu_dict = {"main_menu": ["Exit", "CRUD operations", "Show top ten companies by criteria"],
#              "crud_menu": ["Back", "Create a company", "Read a company", "Update a company"],
#              "topten_menu": ["Back", "List by ND/EBITDA", "List by ROE", "List by ROA"] }
menu_dict = [["Exit", "CRUD operations", "Show top ten companies by criteria"],
             ["Back", "Create a company", "Read a company", "Update a company", "Delete a company", "List all companies"],
             ["Back", "List by ND/EBITDA", "List by ROE", "List by ROA"] ]

menu_name = ["MAIN MENU", "CRUD MENU", "TOP TEN MENU"]


class cfi_program():
    menu_level = 0

    def ask_and_check(self, maxmenu_num):
        while True:
            print()
            print("Enter an option:")
            try:
                selected_item = int(input())
                break
            except:
                print("Invalid option!")
        return selected_item

    def __init__(self):
        while True:
            menu_list = menu_dict[self.menu_level]
            print(menu_name[self.menu_level])
            for number, name in enumerate(menu_list):
                print(number, name)
            user_input = self.ask_and_check(len(menu_list))

            if user_input == 0 and self.menu_level == 0:
                print("Have a nice day!")
                break

            if user_input == 1 and self.menu_level == 1:
                print(menu_name[self.menu_level])

            self.menu_level = user_input





my_cfi = cfi_program()