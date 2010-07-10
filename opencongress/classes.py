from datetime import date, datetime
import re

class BaseNode(object):
    """
    Base object that all nodes inherit from, constructed by parsing an
    ElementTree node.
    """
    def __init__(self, elem):
        for prop in elem.getchildren():
            setattr(self, prop.tag.replace('-', '_'), deserialize(prop))
    
    def __repr__(self):
        return '<OpenCongress %s object (%s)>' % (
            self.__class__.__name__,
            str(self),
        )


class Person(BaseNode):
    """
    An object representing a senator or representative.
    """
    def __str__(self):
        return self.name


class Commentary(BaseNode):
    """
    An object representing a news item or blog post.
    """
    def __str__(self):
        return self.title


class Bill(BaseNode):
    """
    An object representing a bill.
    """
    def __str__(self):
        try:
            return self.title_full_common
        except AttributeError:
            return '%s.%s' % (self.bill_type.upper(), self.number)


class RollCall(BaseNode):
    """
    An object representing a roll call (results of a vote).
    """
    def __str__(self):
        return self.question


class Issue(BaseNode):
    """
    An object representing a political issue.
    """
    def __str__(self):
        return self.term


class Vote(BaseNode):
    """
    An object representing the results of a vote: a roll call and individual
    persons' votes.
    """
    def __init__(self, elem):
        for prop in elem.getchildren():
            name = prop.tag.replace('-', '_')
            if prop.tag.startswith('person'):
                setattr(self, name, prop.getchildren()[0].text)
            elif prop.tag == 'roll-call':
                roll_call = RollCall(prop)
                setattr(self, name, roll_call)
                self.roll_call_name = str(roll_call)
            else:
                setattr(self, name, deserialize(prop))
    
    def __str__(self):
        return self.roll_call_name


def deserialize(elem):
    """
    Deserializes an OpenCongress XML Node (in form of an xml.etree.ElementTree
    element) into a Python datatype.
    
    In opencongress.classes instead of opencongress.utils to prevent circular
    imports (since BaseNode.__init__() calls deserialize, which requires 
    subclasses of BaseNode).
    """
    
    # If the node has a 'nil' attribute, parse into None/0
    try:
        
        if elem.attrib['nil'] == 'true':
            try:
                if elem.attrib['type'] == 'integer':
                    return 0
                elif elem.attrib['type'] == 'float':
                    return float(0)
            except KeyError:
                return None
        
    except KeyError:
        
        # Overrides based on element name
        
        if elem.tag == 'sponsor':
            elem.attrib['type'] = 'Person'
        
        # These elements use a bizarre, undocumented format:
        # 'd':4 'ca':5 'sen':1 'diann':2,6,8 'feinstein':3,7,9
        # Let's parse that into something more sensible
        if elem.tag == 'fti-titles' or elem.tag == 'fti-names':
            members = {}
            for m in elem.text.split(' '):
                key, value = m.split(':')
                members[key.replace("'", '')] = map(int, value.split(','))
            return members
        
        # If the element has a 'type' attribute, use that to decide
        try:
            
            # Parse into datetime.date object
            if elem.attrib['type'] == 'date':
                year, month, day = map(int, elem.text.split('-'))
                return date(year, month, day)
            
            # Parse into datetime.datetime object
            if elem.attrib['type'] == 'timestamp':
                # Time zone stripped because %z is not well-supported
                # See http://bugs.python.org/issue6641
                # Possible future todo: use dateutil.parser.parse instead
                timezoneless = re.sub(r'[+\-]\d{4} ', '', elem.text)
                return datetime.strptime(timezoneless, '%a %b %d %H:%M:%S %Y')
            
            # Parse into integer
            elif elem.attrib['type'] == 'integer':
                return int(elem.text)
            
            # Parse into float
            elif elem.attrib['type'] == 'float':
                return float(elem.text)
            
            # Parse into array populated with children elements
            elif elem.attrib['type'] == 'array':
                kids = []
                for prop in elem.getchildren():
                    kids.append(deserialize(prop))
                return kids
            
            # Parse into an opencongress.classes.Commentary object
            elif elem.attrib['type'] == 'Commentary':
                return Commentary(elem)
            
            # Parse into an opencongress.classes.Person object
            elif elem.attrib['type'] == 'Person':
                return Person(elem)
            
            # Parse into an opencongress.classes.Vote object
            elif elem.attrib['type'] == 'Vote':
                return Vote(elem)
            
            # Parse into boolean
            elif elem.attrib['type'] == 'boolean':
                if elem.text == 'true':
                    return True
                return False
        
        # Since there's no type attribute, we'll try to guess.
        except KeyError:
            
            # If it has children, parse into a dictionary
            if len(elem.getchildren()):
                kids = {}
                for prop in elem.getchildren():
                    kids[prop.tag.replace('-', '_')] = deserialize(prop)
                return kids
            
            # Nothing left but to return a string.
            return elem.text