from pymongo import monitoring

from db_collections import Order, OrderItem, StatusChange
from utils import Menu, Option, Utilities, CommandLogger, select_general, unique_general, prompt_for_date, log
from menu_definitions import menu_main, add_select, list_select, select_select, delete_select, update_select

"""
This protects Order from deletions in OrderItem of any of the objects reference by Order
in its order_items list.  We could not include this in Order itself since that would 
make a cyclic delete_rule between Order and OrderItem.  I've commented this out because
it makes it impossible to remove OrderItem instances.  But you get the idea how it works."""
# OrderItem.register_delete_rule(Order, 'orderItems', mongoengine.DENY)


def menu_loop(menu: Menu):
    """Little helper routine to just keep cycling in a menu until the user signals that they
    want to exit.
    :param  menu:   The menu that the user will see."""
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)


def add():
    menu_loop(add_select)


def list_members():
    menu_loop(list_select)


def select():
    menu_loop(select_select)


def delete():
    menu_loop(delete_select)


def update():
    menu_loop(update_select)


def select_order() -> Order:
    return select_general(Order)


def select_order_item() -> OrderItem:
    return select_general(OrderItem)


def prompt_for_enum(prompt: str, cls, attribute_name: str):
    """
    MongoEngine attributes can be regulated with an enum.  If they are, the definition of
    that attribute will carry the list of choices allowed by the enum (as well as the enum
    class itself) that we can use to prompt the user for one of the valid values.  This
    represents the 'don't let bad data happen in the first place' strategy rather than
    wait for an exception from the database.
    :param prompt:          A text string telling the user what they are being prompted for.
    :param cls:             The class (not just the name) of the MongoEngine class that the
                            enumerated attribute belongs to.
    :param attribute_name:  The NAME of the attribute that you want a value for.
    :return:                The enum class member that the user selected.
    """
    attr = getattr(cls, attribute_name)  # Get the enumerated attribute.
    if type(attr).__name__ == 'EnumField':  # Make sure that it is an enumeration.
        enum_values = []
        for choice in attr.choices:  # Build a menu option for each of the enum instances.
            enum_values.append(Option(choice.value, choice))
        # Build an 'on the fly' menu and prompt the user for which option they want.
        return Menu('Enum Menu', prompt, enum_values).menu_prompt()
    else:
        raise ValueError(f'This attribute is not an enum: {attribute_name}')


def add_order():
    """
    Create a new Order instance.
    :return: None
    """
    success: bool = False
    while not success:
        order_date = prompt_for_date('Date and time of the order: ')
        """This is sort of a hack.  The customer really should come from a Customer class, and the 
        clerk who made the sale, but I'm trying to keep this simple to concentrate on relationships."""
        new_order = Order(input('Customer name --> '), order_date, input('Clerk who made the sale --> '))
        violated_constraints = unique_general(new_order)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            # The first 'stats change' is placing the order itself.
            new_order.change_status(
                StatusChange(
                    prompt_for_enum('Select the status:', StatusChange, 'status'),
                    order_date
                )
            )
            try:
                new_order.save()
                success = True
            except Exception as e:
                print('Errors storing the new order:')
                Utilities.print_exception(e)


def add_order_item():
    """
    Add an item to an existing order.
    :return: None
    """
    success: bool = False
    new_order_item: OrderItem
    order: Order
    while not success:
        order = select_order()  # Prompt the user for an order to operate on.
        # Create a new OrderItem instance.
        new_order_item = OrderItem(order, input('Product Name --> '), int(input('Quantity --> ')))
        # Make sure that this adheres to the existing uniqueness constraints.
        # I COULD use print_exception after MongoEngine detects any uniqueness constraint violations, but
        # MongoEngine will only report one uniqueness constraint violation at a time.  I want them all.
        violated_constraints = unique_general(new_order_item)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:
            try:
                # we cannot add the OrderItem to the Order until it's been stored in the database.
                new_order_item.save()
                order.add_item(new_order_item)  # Add this OrderItem to the Order's MongoDB list of items.
                order.save()                    # Update the order in the database.
                success = True                  # Finally ready to call  it good.
            except Exception as e:
                print('Exception trying to add the new item:')
                print(Utilities.print_exception(e))


def update_order():
    """
    Change the status of an existing order by adding another element to the status vector of the order.
    :return: None
    """
    success: bool = False
    # 'Declare' the order variable, more for cosmetics than anything else.
    order: Order
    while not success:
        order = select_order()  # Find an order to modify.
        status_change_date = prompt_for_date('Date and time of the status change: ')
        new_status = prompt_for_enum('Select the status:', StatusChange, 'status')
        try:
            order.change_status(StatusChange(new_status, status_change_date))
            order.save()
            success = True
        except ValueError as VE:
            print('Attempted status change failed because:')
            print(VE)


def delete_order():
    """
    Delete an existing order from the database.
    :return: None
    """
    order = select_order()  # prompt the user for an order to delete
    items = order.orderItems  # retrieve the list of items in this order
    for item in items:
        """The reference from OrderItem back up to Order has a reverse_delete_rule of DENY, which 
        is similar to the RESTRICT option on a relational foreign key constraint.  Which means that
        if I try to delete the order and there are still any OrderItems depending on that order,
        MongoEngine (not MongoDB) will throw an exception."""
        item.delete()
    # Now that all the items on the order are removed, we can safely remove the order itself.
    order.delete()


def delete_order_item():
    """
    Remove just one item from an existing order.
    :return: None
    """
    order = select_order()  # prompt the user for an order to update
    items = order.orderItems  # retrieve the list of items in this order
    menu_items: [Option] = []  # list of order items to choose from
    # Create an ad hoc menu of all the items presently on the order.  Use __str__ to make a text version of each item
    for item in items:
        menu_items.append(Option(item.__str__(), item))
    # prompt the user for which one of those order items to remove, and remove it.
    order.remove_item(Menu('Item Menu', 'Choose which order item to remove', menu_items).menu_prompt())
    # Update the order to no longer include that order item in its MongoDB list of order items.
    order.save()


if __name__ == '__main__':
    print('Starting in main.')
    monitoring.register(CommandLogger())
    db = Utilities.startup()
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    log.info('All done for now.')
