import os

from pymongo import monitoring, errors
from mongoengine import connect

import utils
import collection_classes


def menu_loop(menu: utils.Menu) -> None:
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)


if __name__ == '__main__':
    # TODO: ideally we would have a CollectionClass interface that all classes we make inherit from, but from my initial
    # testing I couldn't get this to work with mongo engine sadly, alongside that interface I would also want one for
    # the embedded documents, this would allow annotations to work better and everything to be seamless, might revisit.

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
        print('Error, invalid password.  Try again.')
        exit()

    main_action: str = ''
    # TODO: I am not a fan of exec so I eventually want to change how the Menu/Option classes work but they work
    # perfectly fine right now so I will just leave it for a later problem.
    while main_action != utils.main_menu.last_action():
        main_action = utils.main_menu.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    command_logger.log.info('All done for now.')
