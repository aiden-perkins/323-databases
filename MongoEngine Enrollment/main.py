import os

from pymongo import monitoring, errors
from mongoengine import connect

from utils import CommandLogger, Menu, main_menu


def menu_loop(menu: Menu) -> None:
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)


if __name__ == '__main__':
    # TODO: add type annotations to everything in functions, maybe also comments

    # TODO: some things may need the reverse delete rule thing
    print('Starting in main.')
    command_logger = CommandLogger()
    monitoring.register(command_logger)

    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    deployment = os.getenv('DEPLOYMENT') + '.' + os.getenv('CLUSTER_HASH')
    cluster = f'mongodb+srv://{username}:{password}@{deployment}.mongodb.net/?retryWrites=true&w=majority'
    client = connect(db='Enrollment', host=cluster)
    try:
        client.server_info()  # Test the connection
    except errors.OperationFailure as e:
        print(e)
        print('Error, invalid password.  Try again.')
        exit()

    main_action: str = ''
    # TODO: I am not a fan of exec so I eventually want to change how the Menu/Option classes work but they work
    # perfectly fine right now so I will just leave it for a later problem.
    while main_action != main_menu.last_action():
        main_action = main_menu.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    command_logger.log.info('All done for now.')
