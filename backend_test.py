import requests
import json
import random
import string
import unittest
import time

# Base URL from frontend/.env
BASE_URL = "https://eac1532e-8915-4a93-a37e-2e30efe01e91.preview.emergentagent.com"
API_URL = f"{BASE_URL}/api"

def random_email():
    """Generate a random email for testing"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@example.com"

def random_name():
    """Generate a random name for testing"""
    first_names = ["John", "Jane", "Alex", "Sarah", "Michael", "Emma"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

class EcommerceBackendTest(unittest.TestCase):
    """Test class for the ecommerce backend API"""
    
    def setUp(self):
        """Set up test data and register a test user"""
        self.test_email = random_email()
        self.test_password = "TestPassword123!"
        self.test_name = random_name()
        
        # Register a test user
        self.register_response = self.register_user(self.test_email, self.test_password, self.test_name)
        
        # Login to get token
        self.login_response = self.login_user(self.test_email, self.test_password)
        self.token = self.login_response.get("access_token")
        
        # Store product data for later tests
        self.products = self.get_products()
        if self.products:
            self.test_product = self.products[0]
    
    def register_user(self, email, password, full_name):
        """Register a new user"""
        url = f"{API_URL}/register"
        data = {
            "email": email,
            "password": password,
            "full_name": full_name
        }
        response = requests.post(url, json=data)
        print(f"Register response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def login_user(self, email, password):
        """Login a user and get JWT token"""
        url = f"{API_URL}/login"
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(url, json=data)
        print(f"Login response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_user_profile(self):
        """Get the current user profile"""
        url = f"{API_URL}/me"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        print(f"Get profile response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_products(self):
        """Get all products"""
        url = f"{API_URL}/products"
        response = requests.get(url)
        print(f"Get products response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_product_by_id(self, product_id):
        """Get a product by ID"""
        url = f"{API_URL}/products/{product_id}"
        response = requests.get(url)
        print(f"Get product by ID response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_categories(self):
        """Get all product categories"""
        url = f"{API_URL}/categories"
        response = requests.get(url)
        print(f"Get categories response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def search_products(self, search_term):
        """Search products by name or description"""
        url = f"{API_URL}/products?search={search_term}"
        response = requests.get(url)
        print(f"Search products response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def filter_products_by_category(self, category):
        """Filter products by category"""
        url = f"{API_URL}/products?category={category}"
        response = requests.get(url)
        print(f"Filter products response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def add_to_cart(self, product_id, quantity=1):
        """Add a product to the cart"""
        url = f"{API_URL}/cart"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "product_id": product_id,
            "quantity": quantity
        }
        response = requests.post(url, json=data, headers=headers)
        print(f"Add to cart response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_cart(self):
        """Get the current user's cart"""
        url = f"{API_URL}/cart"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        print(f"Get cart response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def update_cart_item(self, item_id, quantity):
        """Update a cart item quantity"""
        url = f"{API_URL}/cart/{item_id}?quantity={quantity}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.put(url, headers=headers)
        print(f"Update cart item response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def remove_from_cart(self, item_id):
        """Remove an item from the cart"""
        url = f"{API_URL}/cart/{item_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.delete(url, headers=headers)
        print(f"Remove from cart response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    def clear_cart(self):
        """Clear the entire cart"""
        url = f"{API_URL}/cart"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.delete(url, headers=headers)
        print(f"Clear cart response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    
    # Test cases
    
    def test_01_user_registration(self):
        """Test user registration"""
        # Registration already happened in setUp
        self.assertIsNotNone(self.register_response)
        self.assertEqual(self.register_response["email"], self.test_email)
        self.assertEqual(self.register_response["full_name"], self.test_name)
        print("✅ User registration test passed")
    
    def test_02_user_login(self):
        """Test user login and JWT token generation"""
        self.assertIsNotNone(self.login_response)
        self.assertIn("access_token", self.login_response)
        self.assertEqual(self.login_response["token_type"], "bearer")
        print("✅ User login test passed")
    
    def test_03_user_profile(self):
        """Test getting user profile with JWT token"""
        profile = self.get_user_profile()
        self.assertIsNotNone(profile)
        self.assertEqual(profile["email"], self.test_email)
        self.assertEqual(profile["full_name"], self.test_name)
        print("✅ User profile test passed")
    
    def test_04_products_listing(self):
        """Test getting all products"""
        self.assertIsNotNone(self.products)
        self.assertGreaterEqual(len(self.products), 15)  # Should have at least 15 products
        print("✅ Products listing test passed")
    
    def test_05_product_detail(self):
        """Test getting a single product by ID"""
        if not self.products:
            self.skipTest("No products available to test")
        
        product_id = self.products[0]["id"]
        product = self.get_product_by_id(product_id)
        
        self.assertIsNotNone(product)
        self.assertEqual(product["id"], product_id)
        self.assertIn("name", product)
        self.assertIn("price", product)
        self.assertIn("description", product)
        self.assertIn("category", product)
        print("✅ Product detail test passed")
    
    def test_06_categories(self):
        """Test getting product categories"""
        categories = self.get_categories()
        self.assertIsNotNone(categories)
        self.assertIn("categories", categories)
        self.assertGreater(len(categories["categories"]), 0)
        print("✅ Categories test passed")
    
    def test_07_search_products(self):
        """Test searching products"""
        if not self.products:
            self.skipTest("No products available to test")
        
        # Search for a term that should be in at least one product
        search_term = self.products[0]["name"].split()[0]
        search_results = self.search_products(search_term)
        
        self.assertIsNotNone(search_results)
        self.assertGreater(len(search_results), 0)
        print("✅ Product search test passed")
    
    def test_08_filter_by_category(self):
        """Test filtering products by category"""
        if not self.products:
            self.skipTest("No products available to test")
        
        # Get a category from the first product
        category = self.products[0]["category"]
        filtered_products = self.filter_products_by_category(category)
        
        self.assertIsNotNone(filtered_products)
        self.assertGreater(len(filtered_products), 0)
        for product in filtered_products:
            self.assertEqual(product["category"], category)
        print("✅ Category filtering test passed")
    
    def test_09_add_to_cart(self):
        """Test adding a product to the cart"""
        if not self.products:
            self.skipTest("No products available to test")
        
        product_id = self.products[0]["id"]
        cart_item = self.add_to_cart(product_id, 2)
        
        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item["product"]["id"], product_id)
        self.assertEqual(cart_item["quantity"], 2)
        print("✅ Add to cart test passed")
    
    def test_10_get_cart(self):
        """Test getting the user's cart"""
        if not self.products:
            self.skipTest("No products available to test")
        
        # First add an item to the cart
        product_id = self.products[0]["id"]
        self.add_to_cart(product_id, 1)
        
        # Then get the cart
        cart = self.get_cart()
        
        self.assertIsNotNone(cart)
        self.assertGreater(len(cart), 0)
        self.assertEqual(cart[0]["product"]["id"], product_id)
        print("✅ Get cart test passed")
    
    def test_11_update_cart_item(self):
        """Test updating a cart item quantity"""
        if not self.products:
            self.skipTest("No products available to test")
        
        # First add an item to the cart
        product_id = self.products[0]["id"]
        cart_item = self.add_to_cart(product_id, 1)
        
        # Then update its quantity
        item_id = cart_item["id"]
        update_response = self.update_cart_item(item_id, 3)
        
        self.assertIsNotNone(update_response)
        self.assertIn("message", update_response)
        
        # Verify the update
        cart = self.get_cart()
        updated_item = next((item for item in cart if item["id"] == item_id), None)
        self.assertIsNotNone(updated_item)
        self.assertEqual(updated_item["quantity"], 3)
        print("✅ Update cart item test passed")
    
    def test_12_remove_from_cart(self):
        """Test removing an item from the cart"""
        if not self.products:
            self.skipTest("No products available to test")
        
        # First add an item to the cart
        product_id = self.products[0]["id"]
        cart_item = self.add_to_cart(product_id, 1)
        
        # Then remove it
        item_id = cart_item["id"]
        remove_response = self.remove_from_cart(item_id)
        
        self.assertIsNotNone(remove_response)
        self.assertIn("message", remove_response)
        
        # Verify the removal
        cart = self.get_cart()
        removed_item = next((item for item in cart if item["id"] == item_id), None)
        self.assertIsNone(removed_item)
        print("✅ Remove from cart test passed")
    
    def test_13_clear_cart(self):
        """Test clearing the entire cart"""
        if not self.products:
            self.skipTest("No products available to test")
        
        # First add a couple items to the cart
        self.add_to_cart(self.products[0]["id"], 1)
        if len(self.products) > 1:
            self.add_to_cart(self.products[1]["id"], 2)
        
        # Then clear the cart
        clear_response = self.clear_cart()
        
        self.assertIsNotNone(clear_response)
        self.assertIn("message", clear_response)
        
        # Verify the cart is empty
        cart = self.get_cart()
        self.assertEqual(len(cart), 0)
        print("✅ Clear cart test passed")
    
    def test_14_duplicate_registration(self):
        """Test that duplicate email registration fails"""
        duplicate_response = requests.post(
            f"{API_URL}/register", 
            json={
                "email": self.test_email,
                "password": "AnotherPassword123!",
                "full_name": "Duplicate User"
            }
        )
        self.assertEqual(duplicate_response.status_code, 400)
        print("✅ Duplicate registration test passed")
    
    def test_15_invalid_login(self):
        """Test that invalid login credentials fail"""
        invalid_response = requests.post(
            f"{API_URL}/login", 
            json={
                "email": self.test_email,
                "password": "WrongPassword123!"
            }
        )
        self.assertEqual(invalid_response.status_code, 401)
        print("✅ Invalid login test passed")
    
    def test_16_protected_route_without_token(self):
        """Test that protected routes require authentication"""
        response = requests.get(f"{API_URL}/me")
        self.assertEqual(response.status_code, 403)
        print("✅ Protected route test passed")
    
    def test_17_invalid_product_id(self):
        """Test that invalid product ID returns 404"""
        response = requests.get(f"{API_URL}/products/invalid-id")
        self.assertEqual(response.status_code, 404)
        print("✅ Invalid product ID test passed")

if __name__ == "__main__":
    # Run the tests
    print(f"Testing backend API at: {API_URL}")
    print("=" * 80)
    
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add all tests in order
    for i in range(1, 18):
        test_name = f"test_{i:02d}_" + getattr(EcommerceBackendTest, f"test_{i:02d}_").__doc__.split()[0].lower()
        suite.addTest(EcommerceBackendTest(test_name))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ All backend tests passed successfully!")
    else:
        print("\n❌ Some tests failed. See details above.")