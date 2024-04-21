import io
import datetime
from pprint import pformat

from mongoengine import NotUniqueError, ValidationError

from utils import Option, Menu


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


def prompt_for_date(prompt: str) -> datetime:
    """
    Prompts the user for a complete date/time.  This will keep prompting the user
    until they provide a valid date time stamp.
    :param prompt: The text to display when prompting the user for the date time stamp.
    :return: An instance of datetime.
    """
    # TODO: Allow the user to default to the current date & time to save time.
    print(prompt)
    valid = False
    while not valid:
        try:
            year: int = int(input('Enter year --> '))
            month: int = int(input('Enter month number --> '))
            day: int = int(input('Enter day number --> '))
            hour: int = int(input('Enter hour (24 hour clock) --> '))
            minute: int = int(input('Enter minute number --> '))
            second: int = int(input('Enter second number --> '))
            return datetime.datetime(year, month, day, hour, minute, second)
        except ValueError as ve:
            print('Error on input: ', ve)
            print('Please try again.')


def get_attr_from_column(cls, column_name) -> str:
    """
    Returns the name of the attribute that corresponds to the given column name.  The attribute
    name is in CamelCase, while the column name is in snake_case.  The column within a Document
    class has the db_field property that gives us the database column name of that attribute.
    :param cls:             The class that has an attribute corresponding to the given column_name.
    :param column_name:     The column that we are looking for the corresponding attribute.
    :return:                THe name of the attribute for the given column.
    """
    for attribute in cls.__dict__['_fields'].keys():
        # the 'id' attribute is a legitimate attribute with a db_name of _id, so we'll use it if need be.
        # if attribute != 'id':  # Skip the obligatory id field
        # TODO: I'm not sure what happens with a dict or list attribute in the class.
        if getattr(cls, attribute).__dict__['db_field'] == column_name:
            return attribute


def select_general(cls):
    """
    Return one instance of the class that's supplied as an input, by prompting the user for
    the values of the selected uniqueness constraint for the collection corresponding to that class.
    :param cls: The class that the user wants a single instance of.
    :return: The instance that the user selected.
    """
    # If we were doing this directly in mongodb, we'd say collection=db[whatever collection it is]
    collection = cls._get_collection()
    index_info = collection.index_information()
    # Loop through the indexes of the collection.
    choices = []
    for index in index_info.keys():
        # see if the index is unique.  If not, we're not interested in using it.
        # _id_ does not have a property named unique since _id_ is ALWAYS unique.  Hence, the order in the if statement.
        if index == '_id_' or index_info[index]['unique']:
            columns = [col[0] for col in index_info[index]['key']]
            choices.append(Option(f'index: {index} - cols: {columns}', index))
    index_menu = Menu('which index', 'Which index do you want to search by:', choices)
    while True:
        # What happens if there are no unique indexes at all?
        chosen_index = index_menu.menu_prompt()
        filters = {}  # The attribute/value pairs that we're going to search by
        for column in [col[0] for col in index_info[chosen_index]['key']]:
            # now I have to convert from the column name to the attribute name.
            attribute_name = get_attr_from_column(cls, column)
            # If this attribute is a reference, we need to go find that referenced document.
            attribute = getattr(cls, attribute_name)
            if type(attribute).__name__ == 'ReferenceField':
                # This attribute in this uniqueness requirement is a reference --> it's an identifying relationship.
                # Now we have to figure out the class that we're referencing.
                referenced_class = attribute.document_type
                # Use my general selection utility to find an instance of the referenced parent
                target = select_general(referenced_class)
                # and add the filter to point to the selected document in the parent collection.
                # I could have just said: filters[attribute_name] = select_general(attribute.document_type)
                filters[attribute_name] = target
                """
                This is intentionally recursive.  If A is a parent to B and B has a reference to A,
                and that reference is part of the uniqueness constraint in B that we are using to select 
                an instance of B, and B is a parent to C and C has a reference to B, and we want to select
                an instance of C based on the 'migrated' reference to B, then you see where the 
                recursion comes in very handy.
                """
            elif type(attribute).__name__ == 'DateTimeField':
                filters[attribute_name] = prompt_for_date(f'search for {attribute_name} =:')
            else:
                # It's not a reference, so prompt for the literal value.
                # This works for string and numeric, but honestly, I should convert the string depending on the type.
                filters[attribute_name] = input(f'search for {attribute_name} = --> ')
        # count the number of rows that meet that criteria.
        if cls.objects(**filters).count() == 1:
            return cls.objects(**filters).first()
        else:
            print('Sorry, no rows found that match those criteria.  Try again.')


def unique_general(instance):
    """
    Check all uniqueness constraints on the collection that instance belongs to and return those
    uniqueness constraints that have been violated.  If that returned list has no members, then
    the instance does not duplicate any documents already in the collection, and it is safe to
    save that instance.
    :param instance:    An instance of a MongoEngine class that the user want to test against all
                        uniqueness constraints on that collection.
    :return:            A list of the 0 or more uniqueness constraints that have been violated.
    """
    # If we were doing this directly in mongodb, we'd say collection=db[whatever collection it is]
    cls = instance.__class__  # get the class from the instance.
    collection = cls._get_collection()  # Get the collection corresponding to that class.
    index_info = collection.index_information()  # get a list of all indexes on that collection.
    # Loop through the indexes of the collection.
    constraints = []
    violated_constraints = []
    for index in index_info.keys():  # Loop through the list of index names.
        # see if the index is unique.  If not, we're not interested in using it.
        # _id_ does not have a property named unique since _id_ is ALWAYS unique.
        # Normally, _id_ is assigned by MongoDB, but the user COULD use that for a descriptive
        # attribute, which COULD mean that there is a document with that _id_ value already.
        if index == '_id_' or index_info[index]['unique']:
            # harvest the list of column names from this index.
            columns = [col[0] for col in index_info[index]['key']]
            # add the name of the index & the column list to our constraints list of dictionaries.
            constraints.append({'name': index, 'columns': columns})
    for constraint in constraints:
        # What happens if there are no unique indexes at all?
        filters = {}  # The attribute/value pairs that we're going to search by
        for column in constraint['columns']:
            # now I have to convert from the column name to the attribute name.
            attribute_name = get_attr_from_column(cls, column)
            # Add the next key=value pair to our list of filters.
            filters[attribute_name] = instance[attribute_name]
        # count the number of rows that meet those criteria.
        if cls.objects(**filters).count() == 1:
            # there is a document in the collection that matches the supplied instance on all attributes
            # of this uniqueness constraint.  So we have another uniqueness constraint violation.
            violated_constraints.append(constraint)
    # If the returned list of violated constraints == [], we know that we are good to insert this object.
    return violated_constraints


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
