import unittest
import json
from inventory_management_search_optimized import Inventory, Product


class TestProduct(unittest.TestCase):
    def test_init(self):
        """Test for Product initalization"""
        self.assertIsInstance(Product("A10","TestName",300,1),Product)

    def test_init_validate_id(self):
        """Test for Product id validaiton"""
        with self.assertRaises(ValueError):
            Product("","TestName",300,1)
    
    def test_init_validate_name(self):
        """Test for Product name validaiton"""
        with self.assertRaises(TypeError):
            Product("A10",123,300,1)

    def test_init_validate_price(self):
        """Test for Product price validaiton"""
        with self.assertRaises(ValueError):
            Product("A10","TestName",-300,1)

    def test_init_validate_quantity(self):
        """Test for Product quantity validaiton"""
        with self.assertRaises(ValueError):
            Product("A10","TestName",300,-1)

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.testInventory=Inventory(load_from_backup=True)
        self.backupFilePath="data/backup_test.json"

    def test_init(self):
        """Test for Inventory initalization"""
        mobile_inventory=Inventory(load_from_backup=False)
        self.assertIsInstance(mobile_inventory,Inventory)
        self.assertEqual(len(mobile_inventory.items),0,"Inventory initialized with 0 items")

    def test_init_load_from_backup(self):
        """Test for Inventory load from backup"""
        mobile_inventory=Inventory(load_from_backup=True)
        with open(self.backupFilePath, "r") as file:
            data=json.load(file)
        self.assertEqual(len(mobile_inventory.items),len(data))

    def test_save_data(self):
        """Test to save Inventory data to backup"""
        mobile_inventory=Inventory(load_from_backup=True)
        mobile_inventory.save_data()
        with open(self.backupFilePath, "r") as file:
            data=json.load(file)
        self.assertEqual(len(mobile_inventory.items),len(data),"Saved succesfully")

    def test_search_by_id(self):
        """Test for Inventory search by ID"""
        self.assertTrue(self.testInventory.search_by_id('A1'))
    
    def test_search_by_id_notexists(self):
        """Test for Inventory search by ID, not exists"""
        self.assertFalse(self.testInventory.search_by_id('B1'))

    def test_add_item(self):
        """Test for Inventory add item"""
        self.testInventory.add_item(Product("A10","TestName",300,1))
        self.assertIsNotNone(self.testInventory.search_by_id("A10"))

    def test_update_item(self):
        """Test for Inventory update item"""
        self.testInventory.update_item(Product("A1","iPhone 18",300,1))
        result=self.testInventory.search_by_id("A1")
        self.assertEqual(result.name,"iPhone 18")
    
    def test_delete_item(self):
        """Test for Inventory delete item"""
        self.assertTrue(self.testInventory.delete_item("A6"))
        
    
    def test_search_everywhere_by_keyboard(self):
        """Test for Inventory search globally by keyword"""
        result=self.testInventory.search_everywhere_by_keyboard("iPhone")
        self.assertEqual(len(result),1)

# Test product class
suite = unittest.TestLoader().loadTestsFromTestCase(TestProduct)
unittest.TextTestRunner(verbosity=2,buffer=True).run(suite)

# Test Inventory class
suite = unittest.TestLoader().loadTestsFromTestCase(TestInventory)
unittest.TextTestRunner(verbosity=2,buffer=True).run(suite)
