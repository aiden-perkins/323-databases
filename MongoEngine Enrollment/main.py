import os

from pymongo import monitoring, errors
from mongoengine import connect

import utils
import collection_documents


def menu_loop(menu: utils.Menu) -> None:
    """
    Little helper routine to just keep cycling in a menu until the user signals
    that they want to exit.

    :param  menu:   The menu that the user will see.
    """
    action: str = ''
    while action != menu.last_action():
        try:
            action = menu.menu_prompt()
            print('next action: ', action)
            exec(action)
        except Exception as ex:
            if str(ex) != 'exit_menu':
                raise ex
            return


if __name__ == '__main__':
    print('Starting in main.')
    command_logger = utils.CommandLogger()
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
        print('Error, invalid password. Try again.')
        exit()

    main_action: str = ''
    while main_action != utils.main_menu.last_action():
        main_action = utils.main_menu.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    command_logger.log.info('All done for now.')
