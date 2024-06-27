import os
import json
class Product:
    def __init__(self,id, name, price, quantity) -> None:
        self.id=id
        self.name=name
        self.price=price
        self.quantity=quantity

    # Print object in user readable format
    def __str__(self) -> str:
        return '{0.name} (Id: {0.id}, Quantity: {0.quantity}, Price: {0.price})'.format(self)
    
    def __repr__(self) -> str:
        return 'Product({0.id!r},{0.name!r},{0.price!r},{0.quantity!r})'.format(self)
    
    #Getters
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def price(self):
        return self._price
    @property
    def quantity(self):
        return self._quantity
    
    #Setters with validations
    @id.setter
    def id(self,value):
        if (value == None):
            raise ValueError("id cannot be None")
        self._id=value
    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise TypeError("Name must be string")
        self._name=value
    @price.setter
    def price(self,value):
        if not isinstance(value,float):
            raise TypeError("Price must be a number")
        elif value<0:
            raise ValueError("Price cannot be negative")
        self._price=value
    @quantity.setter
    def quantity(self,value):
        if not isinstance(value,int):
            raise TypeError("Quantity must be a number")
        elif value<0:
            raise ValueError("Quantity cannot be negative")
        self._quantity=value
    


class Inventory:
    def __init__(self,load_from_backup=True,low_alert_threshold=2) -> None:
        self.items={}
        self.low_alert_threshold=low_alert_threshold
        self.__data_filepath="data/backup_optimized.json"
        if(load_from_backup):
            try:
                self.load_data()
                print("Data loaded!")
            except:
                print("Error while loading data")
            
    def __str__(self) -> str:
        return 'Inventory with {0} items'.format(len(self.items))

    # Load Data from JSON and create List of Products
    def load_data(self):
        if os.path.isfile(self.__data_filepath):
            with open(self.__data_filepath, "r") as file:
                data=json.load(file)
                for product_id, product in data.items():
                    product_obj=Product.__new__(Product)
                    for key, value in product.items():
                        setattr(product_obj, key, value)
                    self.items[product_id]=product_obj
    
    # Save Data to JSON
    def save_data(self):
        with open(self.__data_filepath, "w") as file:
            json.dump(self.items,file,default=lambda a: a.__dict__)
            print("Data Saved!")

    # Check if product exists return boolean value
    def product_exists(self, product_id):
        return product_id in self.items
    
    # Operation #1: Add new item
    def add_item(self,new_product:Product):
        self.items[new_product.id]=new_product
        if(new_product.quantity<=2):
            print("⚠ Low inventory alert for {0}".format(new_product))
    
    def prompt_to_add_item(self,id=None):
        if id==None: 
            id=input("Enter id of the product: ")

        if(not self.product_exists(id)): # Check if product already exists in inventory
            name=input("Enter its name: ")
            price=float(input("It's price (in USD): "))
            quantity=int(input("And it's quantity: "))
            new_product=Product(id,name,price,quantity)
            print("="*80)
            self.add_item(new_product)
            print("Added {0} successfully!👍🏻".format(new_product))
            print("="*80+"\n\n")
        else:
            print("Product with given id already exists in the inventory")
            update_inventory=input("Update the existing product? (y/n): ")
            print("\n\n")
            if(update_inventory=="y"):
                self.prompt_to_update_item(id)  


    # Operation #2: Update existing item
    def update_item(self,new_product:Product):
        if(new_product.id in self.items):
            self.items[new_product.id].name=new_product.name
            self.items[new_product.id].id=new_product.id
            self.items[new_product.id].quantity=new_product.quantity
            if(new_product.quantity<=2):
                print("⚠ Low inventory alert for {0}".format(new_product))
        else:
            print("Item not found!")

    def prompt_to_update_item(self,id=None):
        if id==None:
            id=input("Enter id of the product: ")
        
        if(self.product_exists(id)): # Check if product already exists in inventory
            name=input("Enter its new name: ")
            price=float(input("It's new price (in USD): "))
            quantity=int(input("And it's updated quantity: "))
            new_product=Product(id,name,price,quantity) 
            print("="*80)  
            self.update_item(new_product)
            print("Item Updated successfully!")
            print("="*80+"\n\n")
        else:
            print("Product with given id does not exists")
            add_inventory=input("Add new product? (y/n): ")         
            print("\n\n")
            if(add_inventory=="y"):
                self.prompt_to_add_item(id)

    # Operation #3: Delete existing Item
    def delete_item(self,product_id:int):
        del self.items[product_id]

    def prompt_to_delete_item(self):
        id=input("Enter id of the product to be deleted: ")
        
        print("="*80)
        if(self.product_exists(id)):
            self.delete_item(id)
            print("Item Deleted successfully!")
        else:
            print("Product with given id does not exists")
        print("="*80+"\n\n")
    
    
    # Operation #4: Print all Items
    def print_product_list(self):
        print("="*80)
        for item in self.items.values():
            print(item) 
        print("="*80+"\n\n")

    # Operation #5: Print tabular report
    def generate_report(self):
        total_inventory_value=0
        print("="*80)
        print("{: <10} {: <30} {: <10} {: <10} {: <10}".format("Id","Name","Quantity","Price","Alert Status"))
        for id,item in self.items.items():
            print("{: <10} {: <30} {: <10} {: <10} {: <10}".format(item.id,item.name,item.quantity,item.price,"Low 🛑" if item.quantity<=self.low_alert_threshold else "Ok ✅")) 
            total_inventory_value+=item.price*item.quantity
        
        print("="*80)
        print("Total inventory value: ${0}".format(total_inventory_value))
        print("="*80+"\n\n")

    # Operation #6: Search by ID
    def prompt_to_view_item(self):
        id=input("Enter id of the product to be view: ")
        
        print("="*80)
        if(self.product_exists(id)):
            print(self.items[id])
        else:
            print("Product with given id does not exists!")
        print("="*80+"\n\n")
    
    # Operation #7: Search everywhere by keyword
    def search_everywhere_by_keyboard(self,keyword:str):
        matches=[]
        keyword=keyword.lower() #To make the search case-insensitive
        for product_id,item in self.items.items():
            if keyword in str(item.id).lower() or keyword in str(item.name).lower() or keyword in str(item.quantity).lower() or keyword in str(item.price).lower():
                matches.append(item)   
        return matches

    def prompt_to_search_by_keyboard(self):
        keyword=input("Enter keyword to search: ")
        matches=self.search_everywhere_by_keyboard(keyword)
        print("="*80)
        if matches:
            for product in matches:
                print(product)
        else:
            print("No products found matching the keyword.")
        print("="*80+"\n\n")

    # Operation #8: List low stock items
    def prompt_to_list_low_stock(self):
        print("="*80)
        low_stock_found=False
        for item in self.items.values():
            if item.quantity<=self.low_alert_threshold:
                low_stock_found=True
                print(item)
        if(not low_stock_found):
            print("No product with low stock🥳")
        print("="*80+"\n\n")

        

def operation_selector():
    print("Welcome to Inventory Managment System!👋🏻")

    load_from_backup=input("Would like to load your previous data? (y/n): ")
    mobile_inventory=Inventory(load_from_backup=(load_from_backup=="y"))
    while(1):
        print("Please select an operation that you want to perform on your inventory")
        print("1. Add new Product")
        print("2. Update existing Product")
        print("3. Delete existing Product")
        print("4. List all products")
        print("5. Generate Report for all data")
        print("6. Search product by ID")
        print("7. Search Everywhere by keyword")
        print("8. List low stock items")
        print("9. Exit application")

        choice=input("Operation number: ")
        if choice=="1":
            print("Let's add a new product")
            mobile_inventory.prompt_to_add_item()
        elif choice=="2":
            mobile_inventory.prompt_to_update_item()
        elif choice=="3":
            mobile_inventory.prompt_to_delete_item()
        elif choice=="4":
            mobile_inventory.print_product_list()
        elif choice=="5":
            mobile_inventory.generate_report()
        elif choice=="6":
            mobile_inventory.prompt_to_view_item()
        elif choice=="7":
            mobile_inventory.prompt_to_search_by_keyboard()
        elif choice=="8":
            mobile_inventory.prompt_to_list_low_stock()
        elif choice=="9":
            mobile_inventory.save_data()
            break
        else:
            print("Invalid choice! Enter again")


if __name__=="__main__":
    operation_selector()