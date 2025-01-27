class OutOfRange(Exception):
    pass

def check_range(value: int, minimum_valid: int, maximum_valid: int, name = 'Value'):
    '''
    Check the range of a given variable, and ensure that it within the specified (inclusive) range

    Raises OutOfRange error if the value is not within the specified range
    '''

    if value > maximum_valid:
        raise OutOfRange(f'{name} is greater than allowed limit: {value} > {maximum_valid}')
    
    if value < minimum_valid:
        raise OutOfRange(f'{name} is less than the allowed limit: {value} < {minimum_valid}')