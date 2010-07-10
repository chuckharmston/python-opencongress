from xml.etree import ElementTree
import urllib, urllib2, StringIO, gzip

from opencongress.classes import Person, Bill, Issue, Vote
from opencongress import utils, exceptions


class ApiCall(object):
    
    _valid_kwargs = None
    _valid_values = None
    _url_postfix = None
    
    def __init__(self, key, *args, **kwargs):
        
        self.posargs = args
        self.urlargs = kwargs
        self.validate_args(kwargs)
        
        kwargs['key'] = key
        
        req = urllib.urlopen(self.url)
        
        if req.getcode() != 200:
            raise exceptions.HTTPError(req.getcode())
        
        # Decode gzipped data if it returns gzipped (it seems to happen
        # intermittently)
        try:
            if req.headers['content-encoding'] == 'gzip':
                compressed = StringIO.StringIO(req.read())
                unzipped = gzip.GzipFile(fileobj=compressed)
                self.xml = ElementTree.fromstring(unzipped.read())
            else:
                self.xml = ElementTree.fromstring(req.read())
        except KeyError:
            self.xml = ElementTree.fromstring(req.read())
        
        req.close()
        self.results = self.process()
    
    def validate_args(self, kwargs):
        if self._valid_kwargs:
            
            inv = set(kwargs.keys()) - set(self._valid_kwargs)
            if(len(inv)):
                raise exceptions.ArgumentError('Invalid argument(s): "%s"' % \
                    ', '.join(inv))
                    
            if self._valid_values:
                
                for key, value in kwargs.items():
                    try:
                        if value not in self._valid_values[key]:
                            raise exceptions.ArgumentError(
                                'Invalid argument value: "%s" for "%s"' % \
                                (value, key,)
                            )
                    except KeyError:
                        # If _valid_values[key] is not specified, any 
                        # value is an acceptable value
                        pass
    
    @property
    def url(self):
        return 'http://www.opencongress.org/api/%s?%s' % (
            self._url_postfix,
            urllib.urlencode(self.urlargs)
        )
    
    def process(self):
        pass


class People(ApiCall):
    _url_postfix = 'people'
    _valid_kwargs = 'first_name last_name person_id gender state district \
                    party user_approval_from user_approval_to'.split()
    _valid_values = {
        'gender': 'M F'.split(),
        'state': (
            'AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD '
            'MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD '
            'TN TX UT VT VA WA WV WI WY'
        ).split(),
        'party': 'Republican Democrat Independent'.split()
    }
    
    def __init__(self, key, *args, **kwargs):
        try:
            low, high = kwargs['user_approval']
            if low > high:
                low, high = high, low
            kwargs['user_approval_from'] = low
            kwargs['user_approval_to'] = high
            del kwargs['user_approval']
        except KeyError:
            pass
        super(People, self).__init__(key, *args, **kwargs)
    
    @property
    def url(self):
        return 'http://www.opencongress.org/api/%s?%s' % (self._url_postfix, \
               urllib.urlencode(self.urlargs))
    
    def process(self):
        return [Person(elem) for elem in self.xml.findall('person')]


class SenatorsMostInTheNewsThisWeek(People):
    _url_postfix = 'senators_most_in_the_news_this_week'
    _valid_kwargs = None


class RepresentativesMostInTheNewsThisWeek(People):
    _url_postfix = 'representatives_most_in_the_news_this_week'
    _valid_kwargs = None


class MostBloggedSenatorsThisWeek(People):
    _url_postfix = 'most_blogged_senators_this_week'
    _valid_kwargs = None


class MostBloggedRepresentativesThisWeek(People):
    _url_postfix = 'most_blogged_representatives_this_week'
    _valid_kwargs = None


class CompareTwoPeople(ApiCall):
    _valid_kwargs = 'person1 person2'.split()
    
    @property
    def url(self):
        return 'http://www.opencongress.org/person/compare.xml?%s' \
            % urllib.urlencode(self.urlargs)
    
    def process(self, results={}):
        return {
            'person1': Person(self.xml.find('person1').getchildren()[0]),
            'person2': Person(self.xml.find('person2').getchildren()[0]),
            'hot_votes': [Vote(elem) for elem in \
                self.xml.find('hot_votes').getchildren()],
            'other_votes': [Vote(elem) for elem in \
                self.xml.find('other_votes').getchildren()]
        }


class Bills(ApiCall):
    _url_postfix = 'bills'
    _valid_kwargs = 'type congress number'.split()
    _valid_values = {
        'type': 'h s hj sj hc sc hr sr'.split()
    }
    
    def process(self):
        return [Bill(elem) for elem in self.xml.findall('bill')]


class BillsByIdent(Bills):
    _url_postfix = 'bills_by_ident'
    _valid_kwargs = None
    
    @property
    def url(self):
        return 'http://www.opencongress.org/api/%s?%s&%s' % (
            self._url_postfix,
            urllib.urlencode(self.urlargs),
            '&'.join(['ident[]=%s' % ident for ident in self.posargs]),
        )


class BillsIntroducedSince(Bills):
    _url_postfix = 'bills_introduced_since'
    _valid_kwargs = 'date'.split()


class BillsByQuery(Bills):
    _url_postfix = 'bills_by_query'
    _valid_kwargs = 'q'.split()


class HotBills(Bills):
    _url_postfix = 'hot_bills'
    _valid_kwargs = None


class MostBloggedBillsThisWeek(Bills):
    _url_postfix = 'most_blogged_bills_this_week'
    _valid_kwargs = None


class BillsInTheNewsThisWeek(Bills):
    _url_postfix = 'bills_in_the_news_this_week'
    _valid_kwargs = None


class MostTrackedBillsThisWeek(Bills):
    _url_postfix = 'most_tracked_bills_this_week'
    _valid_kwargs = None


class MostSupportedBillsThisWeek(Bills):
    _url_postfix = 'most_supported_bills_this_week'
    _valid_kwargs = None


class MostOpposedBillsThisWeek(Bills):
    _url_postfix = 'most_opposed_bills_this_week'
    _valid_kwargs = None


class MixedResultSet(ApiCall):
    
    @property
    def url(self):
        return 'http://www.opencongress.org/api/%s/%s?%s' % (
            self._url_postfix,
            self.posargs[0],
            urllib.urlencode(self.urlargs)
        )
    
    def process(self, results={}):
        for result_set in self.xml.getchildren():
            results[result_set.tag] = utils.parse_mixed_result(result_set)
        return results

    
class UsersSupportingPersonAreAlso(MixedResultSet):
    _url_postfix = 'opencongress_users_supporting_person_are_also'


class UsersOpposingPersonAreAlso(MixedResultSet):
    _url_postfix = 'opencongress_users_opposing_person_are_also'


class UsersTrackingPersonAreAlso(MixedResultSet):
    _url_postfix = 'opencongress_users_tracking_person_are_also_tracking'


class UsersSupportingBillAreAlso(MixedResultSet):
    _url_postfix = 'opencongress_users_supporting_bill_are_also'


class UsersOpposingBillAreAlso(MixedResultSet):
    _url_postfix = 'opencongress_users_opposing_bill_are_also'


class UsersTrackingBillAreAlsoTracking(MixedResultSet):
    _url_postfix = 'opencongress_users_tracking_bill_are_also_tracking'


class Issues(ApiCall):
    _url_postfix = 'issues_by_keyword'
    _valid_kwargs = 'keyword'.split()
    
    def process(self):
        return [Issue(elem) for elem in self.xml.findall('subject')]


class BattleRoyale(ApiCall):
    _valid_kwargs = 'timeframe page order sort'.split()
    _valid_values = {
        'timeframe': '1day 5days 30days 1year'.split(),
        'order': 'asc desc'.split(),
        'sort': 'bookmark_count_1 total_comments'.split()
    }
    
    def __init__(self, key, search_type, *args, **kwargs):
        self._search_type = search_type
        super(BattleRoyale, self).__init__(key, *args, **kwargs)
    
    def validate_args(self, kwargs):
        try:            
            if self._search_type == 'bills':
                self._valid_values['sort'] += \
                    'vote_count_1 current_support_pb'.split()
            if self._search_type in ['senators', 'representatives']:
                self._valid_values['sort'] += \
                    'p_approval_count p_approval_avg'.split()
        except KeyError:
            pass
        super(BattleRoyale, self).validate_args(kwargs)
    
    @property
    def url(self):
        if self._search_type == 'bills':
            return 'http://www.opencongress.org/battle_royale.xml?%s' % \
                urllib.urlencode(self.urlargs)
        return 'http://www.opencongress.org/battle_royale/%s.xml?%s' % (
            self._search_type,
            urllib.urlencode(self.urlargs)
        )
    
    def process(self):
        if self._search_type == 'bills':
            return [Bill(elem) for elem in self.xml.findall('bill')]
        elif self._search_type in ['senators', 'representatives']:
            return [Person(elem) for elem in self.xml.findall('person')]
        elif self._search_type == 'issues':
            return [Issue(elem) for elem in self.xml.findall('subject')]