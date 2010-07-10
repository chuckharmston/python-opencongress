from opencongress.classes import *
import re

def url_date(date):
    """
    Takes a datetime.date (or anatidae-ly similar object) and returns a string 
    that the OpenCongress.org API can handle.
    
    >>> import datetime
    >>> url_date(datetime.date(2000, 1, 1))
    'Jan 01st, 2000'
    """
    # Determine the day suffix
    if 4 <= date.day <= 20 or 24 <= date.day <= 30:
        day_suffix = 'th'
    else:
        day_suffix = ['st', 'nd', 'rd'][date.day % 10 - 1]
    
    return date.strftime('%b %d') + day_suffix + date.strftime(', %Y')

def parse_mixed_result(result_set, value=None):
    
    if result_set.tag == 'bill':
        value = Bill(result_set)
    
    elif result_set.tag.startswith('users'):
        value = int(result_set.text)
    
    elif result_set.tag == 'person':
        value = Person(result_set)
    
    elif result_set.tag.endswith('issues'):
        value = [Issue(elem) for elem in result_set.getchildren()]
    
    elif result_set.tag.endswith('bills'):
        value = [Bill(elem) for elem in result_set.getchildren()]
    
    elif result_set.tag.endswith(('senators', 'representatives', 'people')):
        value = [Person(elem) for elem in result_set.getchildren()]
    
    return value