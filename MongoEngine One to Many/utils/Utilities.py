import io
# import getpass
from pprint import pformat
from configparser import ConfigParser

from mongoengine import *
from pymongo.errors import OperationFailure


class Utilities:
    """I have several variations on a theme in this project, and each one will need to start up
    with the same MongoDB database.  So I'm putting any sort of random little utilities in here
    as I need them.

    startup - creates the connection and returns the database client."""

    @staticmethod
    def startup():
        # print('Prompting for the password.')
        while True:
            # password = getpass.getpass(prompt='MongoDB password --> ')
            config = ConfigParser()
            config.read('config.ini')
            usrnme = config['credentials']['db_user']
            passwd = config['credentials']['password']
            dplymnt = config['credentials']['deployment']
            clstr_hash = config['credentials']['cluster_hash']
            cluster = f'mongodb+srv://{usrnme}:{passwd}@{dplymnt}.{clstr_hash}.mongodb.net/?retryWrites=true&w=majority'
            database_name = 'OneToMany'  # input('Database name to use --> ')
            client = connect(db=database_name, host=cluster)
            try:
                client.server_info()  # Test the connection
                return client
            except OperationFailure as OE:
                print(OE)
                print('Error, invalid password.  Try again.')

    @staticmethod
    def print_exception(thrown_exception: Exception):
        """
        Analyze the supplied selection and return a text string that captures what violations of the
        schema & any uniqueness constraints that caused the input exception.  Note that the structure
        of the exception returned from MongoEngine is much simpler in structure than the exceptions
        that we receive from MongoDB, which makes it harder to format the exception message into a
        human-readable format easily.
        :param thrown_exception:    The exception that MongoDB threw.
        :return:                    The formatted text describing the issue(s) in the exception.
        """
        # Use StringIO as a buffer to accumulate the output.
        with io.StringIO() as output:
            output.write('***************** Start of Exception print *****************\n')
            output.write(f'The exception is of type: {type(thrown_exception).__name__}\n')
            # DuplicateKeyError is a subtype of WriteError.  So I have to check for DuplicateKeyError first, and then
            # NOT check for WriteError to get this to work properly.
            if isinstance(thrown_exception, NotUniqueError):
                """As near as I can see, it looks as though the exception thrown by MongoEngine for a violated
                uniqueness constraint only returns the first uniqueness constraint.  So if there are multiple uniqueness
                constraints that the user input violates, this function will only report the first one, which could be
                annoying since the user will not know until the resubmit their input that clears up the first uniqueness
                constraint violation that there are others."""
                error = thrown_exception.args[0]  # get the full text of the error message.
                message = error[error.index('index:') + 7:error.index('}')]  # trim off the unwanted parts
                index_name = message[:message.index(' ')]
                field_list = message[message.index('{') + 2:]  # Extract a string dictionary of the index fields.
                fields_list = []  # The list of fields in the violated uniqueness constraint.
                while field_list.find(':') > 0:  # Keep going until we've gotten all the fields.
                    field_length = field_list.find(':')
                    field = field_list[:field_length]
                    fields_list.append(field)
                    # Trim off the latest field and get ready to get the next field name.
                    if (field_list.find(', ')) > 0:  # at least one more field to report.
                        field_list = field_list[field_list.find(', ') + 2:]
                    else:  # signal that we're done.
                        field_list = ''
                output.write(f'Uniqueness constraint violated: {index_name} with fields:\n{fields_list}')
            elif isinstance(thrown_exception, ValidationError):
                output.write(f'{pformat(thrown_exception.message)}\n')
                all_errors = thrown_exception.errors
                for error in all_errors.keys():
                    output.write(f'field name: {error} has issue: \n{pformat(all_errors.get(error))}\n')
            results = output.getvalue().rstrip()
        return results
