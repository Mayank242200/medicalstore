import re

class Inventory:
    def __init__(self, inventory_file):
        self.inventory_file = inventory_file
        self.load_inventory()

    def load_inventory(self):
        """Load inventory from the file into a dictionary."""
        try:
            self.inventory = {}
            with open(self.inventory_file) as f:
                for line in f:
                    # Debugging: Show the raw line read from the file
                    print(f"Processing line: {line.strip()}")  # Debugging line
                    
                    parts = re.split(r'[,:]', line.strip())  # Split based on comma and colon
                    if len(parts) >= 4:  # Ensure there are enough parts
                        item_code = parts[0].strip()
                        medicine = parts[1].strip()
                        disease = parts[2].strip()
                        
                        # Extract quantity correctly: Find the quantity after 'quantity:' and handle errors
                        quantity_str = parts[3].strip()
                        
                        # Debugging: Show the extracted quantity part
                        print(f"Extracted quantity part: {quantity_str}")  # Debugging quantity extraction

                        if 'quantity' in quantity_str.lower():
                            quantity_match = re.search(r'quantity\s*[:\-]?\s*(\d+)', quantity_str)
                            if quantity_match:
                                quantity = int(quantity_match.group(1))
                                self.inventory[item_code] = {"disease": disease, "medicine": medicine, "quantity": quantity}
                            else:
                                print(f"Error parsing quantity for {item_code}. Using 0 as default.")
                                self.inventory[item_code] = {"disease": disease, "medicine": medicine, "quantity": 0}
                        else:
                            print(f"Error in inventory file for {item_code}. No valid quantity found.")
                            self.inventory[item_code] = {"disease": disease, "medicine": medicine, "quantity": 0}

        except FileNotFoundError:
            print(f"Error: The file {self.inventory_file} was not found.")
            self.inventory = {}

    def find_medicine_by_name(self, medicine_name):
        """Search for a medicine by name in a case-insensitive way."""
        for item_code, details in self.inventory.items():
            if details["medicine"].lower() == medicine_name.lower():  # Case-insensitive search
                return item_code, details
        return None, None

    def update_inventory(self, item_code, quantity):
        """Update the inventory after purchase."""
        if item_code in self.inventory and self.inventory[item_code]["quantity"] >= quantity:
            self.inventory[item_code]["quantity"] -= quantity
            self.save_inventory()
            return True
        return False

    def save_inventory(self):
        """Save the updated inventory back to the file."""
        with open(self.inventory_file, "w") as f:
            for item_code, item_data in self.inventory.items():
                f.write(f"{item_code},{item_data['medicine']},{item_data['disease']},quantity:{item_data['quantity']}\n")

    def add_stock(self, item_code, quantity):
        """Add stock for a specific item."""
        if item_code in self.inventory:
            self.inventory[item_code]["quantity"] += quantity
            self.save_inventory()
        else:
            print("Item not found in inventory.")


class MedicineStore:
    def __init__(self):
        self.inventory = Inventory("inventory.txt")
        self.cart = []
        self.total_amount = 0

    def display_inventory(self):
        """Display all medicines available in the inventory."""
        print("Available Medicines:\n")
        for item_code, details in self.inventory.inventory.items():
            print(f"{item_code}. {details['medicine']} - {details['disease']} - Quantity: {details['quantity']}")

    def purchase_medicine(self):
        """Purchase medicines by name and quantity."""
        print("\nEnter your name:")
        name = input()
        print("Enter your contact number (10 digits):")
        contact_number = input()

        # Validate contact number
        while not re.match(r'^\d{10}$', contact_number):
            print("Invalid contact number. Please enter a valid 10-digit number.")
            contact_number = input()

        print("Enter the name of the medicine you want to purchase:")
        medicine_name = input()

        # Validate medicine name
        item_code, medicine_details = self.inventory.find_medicine_by_name(medicine_name)
        while item_code is None:
            print("Invalid medicine name. Please try again.")
            medicine_name = input()
            item_code, medicine_details = self.inventory.find_medicine_by_name(medicine_name)

        print(f"Enter the quantity (Available: {medicine_details['quantity']}):")
        quantity = input()

        # Validate quantity
        while not quantity.isdigit() or int(quantity) <= 0 or int(quantity) > medicine_details['quantity']:
            print(f"Invalid quantity. Please enter a valid quantity (Available: {medicine_details['quantity']}):")
            quantity = input()

        quantity = int(quantity)  # Convert to integer after validation

        # Add medicine to cart and update inventory
        self.cart.append({"name": medicine_name, "quantity": quantity, "price": 10})  # Assuming price is 10 for simplicity
        self.total_amount += quantity * 10
        self.inventory.update_inventory(item_code, quantity)

        # Ask if the user wants to purchase another item
        print("Do you want to purchase another item? (yes/no):")
        choice = input().lower()
        if choice == "yes":
            self.purchase_medicine()
        else:
            self.generate_bill()

    def generate_bill(self):
        """Generate the final bill after the purchase."""
        print("\nGenerating Bill...")
        print(f"{'SrNo':<5}{'Item Code':<15}{'Medicine':<15}{'Quantity':<10}{'Price':<10}{'Total'}")
        for i, item in enumerate(self.cart, 1):
            total = item["quantity"] * item["price"]
            print(f"{i:<5}{item['name']:<15}{item['quantity']:<10}{item['price']:<10}{total}")
        print(f"\nTotal Amount: {self.total_amount}")
        print(f"Please pay {self.total_amount} INR. Thank you for your purchase!")

    def start(self):
        """Start the store's operations."""
        while True:
            print("\n1. Check available medicines")
            print("2. Purchase medicines")
            print("3. Display updated inventory")
            print("4. Add stock")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.display_inventory()
            elif choice == "2":
                self.purchase_medicine()
            elif choice == "3":
                self.inventory.load_inventory()
                print("\nUpdated Inventory:")
                self.display_inventory()
            elif choice == "4":
                print("Enter item code to add stock:")
                item_code = input()
                print("Enter quantity to add:")
                quantity = int(input())
                self.inventory.add_stock(item_code, quantity)
            elif choice == "5":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    store = MedicineStore()
    store.start()
