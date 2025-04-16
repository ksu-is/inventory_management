# inventory_management
Create a project folder (e.g., inventory_system)
Inside it, create:
  inventory.csv – stores item ID, name, quantity, price
  sales.csv (optional for predictions) – stores date, item ID, and quantity sold
  inventory_gui.py – main script for the GUI
  predict_sales.py (optional) – for forecasting

Create a class to load, save, add, update, and delete inventory using Pandas
  Ensure it reads/writes to inventory.csv
  Validate for duplicate item IDs

Create main window using tkinter.Tk()
  Add a table using ttk.Treeview to display inventory

Add buttons:
  View/Refresh Inventory
  Add Item (popup)
  Update Item (popup)

Delete Selected Item 
 Test adding, updating, deleting items
  Refresh to see changes

