import logging

from utils import Menu, Option

menu_logging = Menu('debug', 'Please select the logging level from the following:', [
    Option('Debugging', logging.DEBUG),
    Option('Informational', logging.INFO),
    Option('Error', logging.ERROR)
])

menu_main = Menu('main', 'Please select one of the following options:', [
    Option('Add new instance', 'menu_loop(add_select)'),
    Option('Delete existing instance', 'menu_loop(delete_select)'),
    Option('List existing instances', 'menu_loop(list_select)'),
    Option('Select existing instance', 'menu_loop(select_select)'),
    Option('Update existing instance', 'menu_loop(update_select)'),
    Option('Exit', 'pass')
])

# options for adding a new instance
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option('Orders', 'add_order()'),
    Option('Products', 'add_product()'),
    Option('Order Items', 'add_order_item()'),
    Option('Exit', 'pass')
])

# options for deleting an existing instance
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option('Orders', 'delete_order()'),
    Option('Products', 'delete_product()'),
    Option('Order Items', 'delete_order_item()'),
    Option('Exit', 'pass')
])

# options for listing the existing instances
list_select = Menu('list select', 'Which type of object do you want to list?:', [
    Option('Orders', 'list_order()'),
    Option('Products', 'list_product()'),
    Option('Order Items', 'list_order_item()'),
    Option('Exit', 'pass')
])

# options for testing the select functions
select_select = Menu('select select', 'Which type of object do you want to select:', [
    Option('Order', 'print(select_order())'),
    Option('Product', 'print(select_product())'),
    Option('Order Item', 'print(select_order_item())'),
    Option('Exit', 'pass')
])

# options for testing the update functions
update_select = Menu('update select', 'Which type of object do you want to update:', [
    Option('Order', 'update_order()'),
    Option('Product', 'update_product()'),
    Option('Exit', 'pass')
])
