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
        self.items=[]
        self.low_alert_threshold=low_alert_threshold
        self.__data_filepath="data/backup.json"
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
                for product in data:
                    product_obj=Product.__new__(Product)
                    for key, value in product.items():
                        setattr(product_obj, key, value)
                    self.items.append(product_obj)
    
    # Save Data to JSON
    def save_data(self):
        if os.path.isfile(self.__data_filepath):
            with open(self.__data_filepath, "w") as file:
                json.dump(self.items,file,default=lambda a: a.__dict__)
                print("Data Saved!")
    
    # Operation #1: Add new item
    def add_item(self,new_product):
        self.items.append(new_product)
    
    def prompt_to_add_item(self):
        id=input("Enter id of the product: ")
        name=input("Enter its name: ")
        price=float(input("It's price (in USD): "))
        quantity=int(input("And it's quantity: "))
        new_product=Product(id,name,price,quantity)

        item_index=self.search_product_by_id(id) # Check if product already exists in inventory
        if(item_index==-1):
            self.add_item(new_product)
            print("Added {0} successfully!👍🏻".format(new_product))
            if(new_product.quantity<=2):
                print("⚠ Low inventory alert for {0}".format(new_product))
            print("==================================================\n\n")
        else:
            print("Product with given id already exists in the inventory")
            update_inventory=input("Update the existing product? (y/n): ")
            if(update_inventory=="y"):
                self.update_item(item_index,new_product)  


    # Operation #2: Update existing item
    def update_item(self,new_product:Product):
        for idx,product in enumerate(self.items):
            if(new_product.id==product.id):
                self.items[idx].name=new_product.name
                self.items[idx].id=new_product.id
                self.items[idx].quantity=new_product.quantity
                break
        print("Item not found!")
        
    def update_item(self,index:int,new_product:Product):
        self.items[index].name=new_product.name
        self.items[index].id=new_product.id
        self.items[index].quantity=new_product.quantity


    def prompt_to_update_item(self):
        id=input("Enter id of the product: ")
        name=input("Enter its new name: ")
        price=float(input("It's new price (in USD): "))
        quantity=int(input("And it's updated quantity: "))
        new_product=Product(id,name,price,quantity)
        
        item_index=self.search_product_by_id(id)
        if(item_index!=-1):
            self.update_item(item_index,new_product)
            print("Item Updated successfully!")
            if(new_product.quantity<=2):
                print("⚠ Low inventory alert for {0}".format(new_product))
            print("==================================================\n\n")
        else:
            print("Product with given id does not exists")
            add_inventory=input("Add new product? (y/n): ")
            print("\n\n")
            if(add_inventory=="y"):
                self.add_item(new_product)

    # Operation #3: Delete existing Item
    def delete_item(self,product_to_be_deleted:Product):
        for idx,product in enumerate(self.items):
            if(product_to_be_deleted.id==product.id):
                self.items.pop(idx)

    def delete_item(self,index:int):
        self.items.pop(index)

    def prompt_to_delete_item(self):
        id=input("Enter id of the product to be deleted: ")
        
        item_index=self.search_product_by_id(id)
        if(item_index!=-1):
            self.delete_item(item_index)
            print("Item Deleted successfully!\n\n")
        else:
            print("Product with given id does not exists\n\n")
    
    
    # Operation #4: Print all Items
    def print_product_list(self,ids=None):
        # If no ids are passed print entire array
        print("==================================================")
        if ids==None:
            for item in self.items:
                print(item) 
        else:
            for item in self.items:
                if item.id in ids:
                    print(item) 
        print("==================================================\n\n")

    # Operation #5: Print tabular report
    def generate_report(self):
        total_inventory_value=0
        print("===============================================================================")
        print("{: <10} {: <30} {: <10} {: <10} {: <10}".format("Id","Name","Quantity","Price","Alert Status"))
        for item in self.items:
            print("{: <10} {: <30} {: <10} {: <10} {: <10}".format(item.id,item.name,item.quantity,item.price,"Low 🛑" if item.quantity<=self.low_alert_threshold else "Ok ✅")) 
            total_inventory_value+=item.price*item.quantity
        
        print("===============================================================================\n\n")
        print("Total inventory value: ${0}\n\n".format(total_inventory_value))

    # Operation #6: Search by ID
    def prompt_to_view_item(self):
        id=input("Enter id of the product to be view: ")
        
        item_index=self.search_product_by_id(id)
        if(item_index!=-1):
            self.print_product_list([id])
        else:
            print("Product with given id does not already exists")

    # Searches inventory for product by product id, if product does not exists returns -1 
    def search_product_by_id(self, product_id):
        for index,product in enumerate(self.items):
            if(product_id==product.id):
                return index
        return -1
    
    # Operation #7: Search everywhere by keyword
    def prompt_to_search_everywhere(self):
        keyword=input("Enter keyword to search: ")
        matches=[]
        for item in self.items:
            if keyword in str(item.id) or keyword in str(item.name) or keyword in str(item.quantity) or keyword in str(item.price):
                matches.append(item.id)
        self.print_product_list(matches)

    # Operation #8: List low stock items
    def prompt_to_list_low_stock(self):
        matches=[]
        for item in self.items:
            if item.quantity<=self.low_alert_threshold:
                matches.append(item.id)
        self.print_product_list(matches)

        

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
            mobile_inventory.prompt_to_search_everywhere()
        elif choice=="8":
            mobile_inventory.prompt_to_list_low_stock()
        elif choice=="9":
            mobile_inventory.save_data()
            break
        else:
            print("Invalid choice! Enter again")


if __name__=="__main__":
    operation_selector()