import io

from pymongo import errors


def check_unique(collection, new_document, column_list) -> bool:
    """
    Validate a document to see whether it duplicates any existing documents already in the collection.
    :param collection:      Reference to the collection that we are about to insert into.
    :param new_document:    The Python dictionary with the data for the new document.
    :param column_list:     The list of columns from the index that we're checking.
    :return:                True if this insert should work wrt to this index, False otherwise.
    """
    find = {}  # initialize the selection criteria.
    # build the search "string" that we'll be searching on.
    # Each element in column_list is a tuple: the column name and whether the column is sorted in ascending
    # or descending order.  I don't care about the direction, just the name of the column.
    for column_name, direction in column_list:
        if column_name in new_document.keys():
            # add the next criteria to the find.  Defaults to a conjunction, which is perfect for this application.
            find[column_name] = new_document[column_name]
    if find:
        # count the number of documents that duplicate this one across the supplied columns.
        return collection.count_documents(find) == 0
    else:
        # All the columns in the index are null in the new document.
        return False


def check_all_unique(collection, new_document):
    """
    Driver for check_unique.  check_unique just looks at one uniqueness constraint for the given collection.
    check_all_unique looks at each uniqueness constraint for the collection by calling check_unique.
    :param collection:
    :param new_document:
    :return:
    """
    # get the index metadata from MongoDB on the sections collection
    collection_ind = collection.index_information()  # Get all the index information
    # Cycle through the indexes one by one.  The variable "index" is just the index name.
    for index in collection_ind:
        if index != '_id_':                 # Skip this one since we cannot control it (usually)
            # Get the list of columns in this index.  The index variable is just the name.
            columns = collection_ind[index]
            if columns['unique']:           # make sure this is a uniqueness constraint
                print(
                    f'Unique index: {index} will be respected: {check_unique(collection, new_document, columns["key"])}'
                )


def print_exception(thrown_exception: Exception):
    """
    Analyze the supplied selection and return a text string that captures what violations of the
    schema & any uniqueness constraints that caused the input exception.
    :param thrown_exception:    The exception that MongoDB threw.
    :return:                    The formatted text describing the issue(s) in the exception.
    """
    # Use StringIO as a buffer to accumulate the output.
    with io.StringIO() as output:
        output.write('***************** Start of Exception print *****************\n')
        # DuplicateKeyError is a subtype of WriteError.  So I have to check for DuplicateKeyError first, and then
        # NOT check for WriteError to get this to work properly.
        if isinstance(thrown_exception, errors.DuplicateKeyError):
            error_message = thrown_exception.details
            # There may be multiple columns in the uniqueness constraint.
            # I'm not sure what happens if there are multiple uniqueness constraints violated at the same insert.
            fields = []
            output.write('Uniqueness constraint violated on the fields:')
            # Get the list of fields in the uniqueness constraint.
            for field in iter(error_message['keyValue']):
                fields.append(field)
            output.write(f'{', '.join(fields)}` should be unique.')
        elif isinstance(thrown_exception, errors.WriteError):
            error_message = thrown_exception.details['errInfo']['details']
            # In case there are multiple criteria violated at the same time.
            for error in error_message['schemaRulesNotSatisfied']:
                # One field could have multiple constraints violated.
                field_errors = error.get('propertiesNotSatisfied')
                if field_errors:
                    for field_error in field_errors:
                        field = field_error['propertyName']
                        reasons = field_error.get('details', [])
                        for reason in reasons:
                            operator_name = reason.get('operatorName')
                            if operator_name == 'enum':
                                allowed_values = reason['specifiedAs']['enum']
                                output.write(
                                    f'Error: Invalid value for field `{field}`. Allowed values are: {allowed_values}\n'
                                )
                            elif operator_name in ['maxLength', 'minLength']:
                                specified_length = reason['specifiedAs'][operator_name]
                                output.write(
                                    f'Error: Invalid length for field `{field}`. '
                                    f'The length should be {operator_name} {specified_length}.\n'
                                )
                            elif operator_name == 'unique':
                                output.write(
                                    f'Error: field `{field}` already exists. Please choose a different value.\n'
                                )
                            elif operator_name == 'combineUnique':
                                fields = reason['specifiedAs']['fields']
                                output.write(f'Error: Combination of fields `{", ".join(fields)}` should be unique.\n')
                            else:
                                output.write(
                                    f'Error: `{reason["reason"]}` for field `{field}`. Please correct the input.\n'
                                )
        results = output.getvalue().rstrip()
    return results
