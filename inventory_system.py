"""
A simple JSON-based inventory management system.
Demonstrates loading, saving, and manipulating stock data.
"""

import json
import logging
from datetime import datetime


class InventorySystem:
    """Manages inventory data, including loading, saving, and modification."""

    def __init__(self):
        """Initializes the inventory system with empty stock data."""
        self.stock_data = {}

    def add_item(self, item="default", qty=0):
        """
        Adds a specified quantity of an item to the stock.

        Args:
            item (str): The name of the item to add.
            qty (int): The quantity to add.
        """
        if not isinstance(item, str) or item == "default":
            logging.warning("Invalid item name provided. Must be a string.")
            return

        if not isinstance(qty, int):
            logging.warning(f"Invalid quantity '{qty}' for item '{item}'. Must be an integer.")
            return

        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        logging.info(f"{datetime.now()}: Added {qty} of {item}")

    def remove_item(self, item, qty):
        """
        Removes a specified quantity of an item from the stock.

        Args:
            item (str): The name of the item to remove.
            qty (int): The quantity to remove.
        """
        if not isinstance(item, str) or not isinstance(qty, int):
            logging.warning(f"Invalid types for remove_item: {item}, {qty}")
            return

        try:
            self.stock_data[item] -= qty
            if self.stock_data[item] <= 0:
                del self.stock_data[item]
                logging.info(f"Removed item '{item}' from stock (quantity zero or less).")
        except KeyError:
            logging.warning(f"Attempted to remove non-existent item: {item}")

    def get_qty(self, item):
        """
        Gets the current quantity of a specific item.

        Args:
            item (str): The name of the item to check.

        Returns:
            int: The quantity of the item, or 0 if not found.
        """
        return self.stock_data.get(item, 0)

    def load_data(self, file="inventory.json"):
        """
        Loads inventory data from a JSON file.

        Args:
            file (str): The filename to load data from.
        """
        try:
            with open(file, "r", encoding="utf-8") as f:
                self.stock_data = json.loads(f.read())
            logging.info(f"Data loaded successfully from {file}")
        except FileNotFoundError:
            logging.warning(f"File not found: {file}. Starting with empty inventory.")
            self.stock_data = {}
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from {file}. Starting with empty inventory.")
            self.stock_data = {}

    def save_data(self, file="inventory.json"):
        """
        Saves the current inventory data to a JSON file.

        Args:
            file (str): The filename to save data to.
        """
        try:
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(self.stock_data, indent=4))
            logging.info(f"Data saved successfully to {file}")
        except IOError as e:
            logging.error(f"Error saving data to {file}: {e}")

    def print_data(self):
        """Prints a formatted report of all items and their quantities."""
        print("\n--- Items Report ---")
        if not self.stock_data:
            print("  (Inventory is empty)")
        for item, qty in self.stock_data.items():
            print(f"  {item} -> {qty}")
        print("--------------------\n")

    def check_low_items(self, threshold=5):
        """
        Finds all items with a quantity below a given threshold.

        Args:
            threshold (int): The stock level to check against.

        Returns:
            list: A list of item names below the threshold.
        """
        return [item for item in self.stock_data if self.stock_data[item] < threshold]


def main():
    """Main function to run the inventory system demo."""
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    inventory = InventorySystem()

    # Load existing data first (if any)
    inventory.load_data()

    inventory.add_item("apple", 10)
    inventory.add_item("banana", 2)  # Changed from -2, assuming additions are positive
    inventory.add_item(123, "ten")  # Will be caught by validation
    inventory.remove_item("apple", 3)
    inventory.remove_item("orange", 1)  # Will be caught by KeyError handler

    print(f"Apple stock: {inventory.get_qty('apple')}")
    print(f"Low items: {inventory.check_low_items()}")

    inventory.save_data()
    inventory.load_data()  # Demonstrate reloading data
    inventory.print_data()


if __name__ == "__main__":
    main()
