import opencongress.calls
import opencongress.exceptions
from opencongress.utils import url_date

class Api(object):
    """
    A Python interface to the OpenCongress.org API.
    
    >>> api = opencongress.Api('api_key_here')
    <opencongress.Api object at 0x000000000>
    
    Parameters
    ==========
    key = Your OpenCongress.org API key. Get one at
        http://www.opencongress.org/api
        
    """
    
    def __init__(self, key):
        try:
            self.key = key
        except NameError:
            raise exceptions.NoApiKeyProvided()
        
    def people(self, *args, **kwargs):
        """
        Queries OpenCongress.org's database of people matching the criteria
        specified in keyword arguments.
        
        Usage
        =====
        >>> api.people(first_name='Edward', last_name='Kennedy')
        
        Returns
        =======
        [
            <OpenCongress Person object>
        ]
        
        Keyword arguments
        =================
        first_name = A string specifying a person's first name
        last_name = A string specifying a person's last name
        person_id = An integer specifying a person's OpenCongress ID
        gender = A string specifying a person's gender (M for male, F for
            female)
        state = A string specifying a person's state (2-letter abbreviation)
        party = A string specifying a person's political party (either 
            'Republican', 'Democrat', or 'Independent')
        user_approval = A two-tuple specifying the low and high ends of the 
            average OpenCongress user's approval rating - e.g.(2.5, 7.5,). 
            Minimum 0.0, maximum 10.0.
        
        """
        return calls.People(self.key, *args, **kwargs).results
    
    def senators_most_in_the_news_this_week(self):
        """
        Returns a list of the senators who have been in the news most frequently
        in the past week.
        
        Usage
        =====
        >>> api.senators_most_in_the_news_this_week()
        
        Returns
        =======
        [
            <OpenCongress Person object>
        ]
        
        """
        return calls.SenatorsMostInTheNewsThisWeek(self.key).results
    
    def representatives_most_in_the_news_this_week(self):
        """
        Returns a list of the representatives who have been in the news most 
        frequently in the past week.
        
        Usage
        =====
        >>> api.representatives_most_in_the_news_this_week()
        
        Returns
        =======
        [
            <OpenCongress Person object>
        ]
        
        """
        return calls.RepresentativesMostInTheNewsThisWeek(self.key).results
    
    def most_blogged_senators_this_week(self):
        """
        Returns a list of the senators who have been blogged about most 
        frequently in the past week.
        
        Usage
        =====
        >>> api.most_blogged_senators_this_week()
        
        Returns
        =======
        [
            <OpenCongress Person object>
        ]

        """
        return calls.MostBloggedSenatorsThisWeek(self.key).results
    
    def most_blogged_representatives_this_week(self):
        """
        Returns a list of the representatives who have been blogged about most 
        frequently in the past week.
        
        Usage
        =====
        >>> api.most_blogged_representatives_this_week()
        
        Returns
        =======
        [
            <OpenCongress Person object>
        ]
        
        """
        return calls.MostBloggedRepresentativesThisWeek(self.key).results
    
    def compare_two_people(self, person1, person2, *args, **kwargs):
        """
        Returns two people and their shared votes.
        
        Arguments
        =========
        person1 = An integer specifying a person's OpenCongress ID
        person2 = An integer specifying a person's OpenCongress ID
        
        Usage
        =====
        >>> api.compare_two_people(300022, 400629)
        
        Returns
        =======
        {
            'person1': <OpenCongress Person object (person1)>,
            'person2': <OpenCongress Person object (person2)>,
            'hot_votes': [
                <OpenCongress Vote object>
            ],
            'other_votes': [
                <OpenCongress Vote object>
            ]
        }
        
        """
        kwargs['person1'] = person1
        kwargs['person2'] = person2
        return calls.CompareTwoPeople(self.key, *args, **kwargs).results
    
    def users_supporting_person_are_also(self, person_id, *args, **kwargs):
        """
        Returns bills and people that are approved or disapproved by 
        OpenCongress users who approve of the person indicated by person_id.
        
        Arguments
        =========
        person_id = An integer specifying a person's OpenCongress ID
        
        Usage
        =====
        >>> api.users_supporting_person_are_also(300042)
        
        Returns
        =======
        {
            'also_approved_representatives': [
                <OpenCongress Person object>
            ],
            'also_approved_senators': [
                <OpenCongress Person object>
            ],
            'also_disapproved_representatives': [
                <OpenCongress Person object>
            ],
            'also_disapproved_senators': [
                <OpenCongress Person object>
            ],
            'also_opposing_bills': [
                <OpenCongress Bill object>
            ],
            'also_supporting_bills': [
                <OpenCongress Bill object>
            ],
            'person': <OpenCongress Person object (person_id)>,
            'users_supporting': 76
        }
        
        """
        return calls.UsersSupportingPersonAreAlso(self.key, person_id, *args, \
            **kwargs).results
    
    def users_opposing_person_are_also(self, person_id, *args, **kwargs):
        """
        Returns bills and people that are approved or disapproved by 
        OpenCongress users who disapprove of the person indicated by person_id.
        
        Arguments
        =========
        person_id = An integer specifying a person's OpenCongress ID
        
        Usage
        =====
        >>> api.users_supporting_person_are_also(412378)
        
        Returns
        =======
        {
            'also_approved_representatives': [
                <OpenCongress Person object>
            ],
            'also_approved_senators': [
                <OpenCongress Person object>
            ],
            'also_disapproved_representatives': [
                <OpenCongress Person object>
            ],
            'also_disapproved_senators': [
                <OpenCongress Person object>
            ],
            'also_opposing_bills': [
                <OpenCongress Bill object>
            ],
            'also_supporting_bills': [
                <OpenCongress Bill object>
            ],
            'person': <OpenCongress Person object (person_id)>,
            'users_supporting': 76
        }
        
        """
        return calls.UsersOpposingPersonAreAlso(self.key, person_id, *args, \
            **kwargs).results
    
    
    def users_tracking_person_are_also(self, person_id, *args, **kwargs):
        """
        Returns bills and people that are tracked by OpenCongress users who 
        track the person indicated by person_id.
        
        Arguments
        =========
        person_id = An integer specifying a person's OpenCongress ID
        
        Usage
        =====
        >>> api.users_tracking_person_are_also(412378)
        
        Returns
        =======
        {
            'tracking_people': [
                <OpenCongress Person object>
            ],
            'tracking_bills': [
                <OpenCongress Bill object>
            ],
            'tracking_issues': [
                <OpenCongress Issue object>
            ],
            'person': <OpenCongress Person object (person_id)>,
        }
        
        """
        return calls.UsersTrackingPersonAreAlso(self.key, person_id, *args, \
            **kwargs).results
    
    
    def bills(self, *args, **kwargs):
        """
        Queries OpenCongress.org's database of bills matching the criteria
        specified in keyword arguments.
        
        Usage
        =====
        >>> api.bills(congress=111)
        
        Returns
        =======
        [
            <OpenCongress Bill object>
        ]
        
        Keyword arguments
        =================
        type = A string specifying a bill's type. Can be "h" (house), "s"
            (senate), "hj" (house joint resolution), "sj" (senate joint 
            resolution), "hc" (house concurrent resolution), "sc" (senate 
            concurrent resolution), "hr" (house resolution), or "sr" (senate 
            resolution) 
        congress = An integer specifying the Congress session
        number = An integer specifying a bill's number
        
        """
        return calls.Bills(self.key, *args, **kwargs).results
    
    def bills_by_ident(self, *args, **kwargs):
        """
        Queries OpenCongress.org's database of bills matching one of the passed
        
        Arguments
        =========
        bill_id = An series of strings specifying bills' OpenCongress IDs
        
        Usage
        =====
        >>> api.bills_by_ident('111-h2454', '111-h3962')
        
        Returns
        =======
        [
            <OpenCongress Bill object (111-h2454)>,
            <OpenCongress Bill object (111-h3962)>
        ]
        
        """
        return calls.BillsByIdent(self.key, *args, **kwargs).results
    
    def bills_introduced_since(self, date_from, *args, **kwargs):
        """
        Queries OpenCongress.org's database of bills introduced since date_from,
        30 at a time.
        
        Arguments
        =========
        date_from = A datetime.date object
        
        Usage
        =====
        >>> date_from = datetime.date(2010, 07, 04)
        >>> api.bills_introduced_since(date_from)
        
        Returns
        =======
        [
            <OpenCongress Bill object>
        ]
        
        """
        kwargs['date'] = url_date(date_from)
        return calls.BillsIntroducedSince(self.key, *args, **kwargs).results
    
    def bills_by_query(self, query, *args, **kwargs):
        """
        Queries OpenCongress.org's database of bills matching the passed query
        
        Arguments
        =========
        query = A string to search by
        
        Usage
        =====
        >>> api.bills_by_query('poverty')
        
        Returns
        =======
        [
            <OpenCongress Bill object>
        ]
        
        """
        kwargs['q'] = query
        return calls.BillsByQuery(self.key, *args, **kwargs).results
    
    def hot_bills(self):
        """
        Returns a list of bills that OpenCongress senators feel are "hot"
        
        Usage
        =====
        >>> api.hot_bills()
        
        Returns
        =======
        [
            <OpenCongress Bill object>
        ]
        
        """
        return calls.HotBills(self.key).results
    
    def most_blogged_bills_this_week(self):
        """
        Returns a list of bills most blogged about in the past week
        
        Usage
        =====
        >>> api.most_blogged_bills_this_week()
        
        Returns
        =======
        [
            <OpenCongress Bill object>
        ]
        
        """
        return calls.MostBloggedBillsThisWeek(self.key).results
    
    def bills_in_the_news_this_week(self):
        """
        Returns a list of bills most discussed in the news in the past week
        
        Usage
        =====
        >>> api.bills_in_the_news_this_week()
        
        Returns
        =======
        [
            <OpenCongress Bill object>
        ]
        
        """
        return calls.BillsInTheNewsThisWeek(self.key).results
    
    def most_tracked_bills_this_week(self):
        """
        Returns a list of bills most tracked on OpenCongress.org in the
        past week
        
        Usage
        =====
        >>> api.most_tracked_bills_this_week()
        
        Returns
        =======
        [
            <OpenCongress Bill object>
        ]
        
        """
        return calls.MostTrackedBillsThisWeek(self.key).results
    
    def most_supported_bills_this_week(self):
        """
        Returns a list of bills most supported on OpenCongress.org in the 
        past week
        
        Usage
        =====
        >>> api.most_supported_bills_this_week()
        
        Returns
        =======
        [
            <OpenCongress Bill object>
        ]
        
        """
        return calls.MostSupportedBillsThisWeek(self.key).results
    
    def most_opposed_bills_this_week(self):
        """
        Returns a list of bills most opposed on OpenCongress.org in the
        past week
        
        Usage
        =====
        >>> api.most_opposed_bills_this_week()
        
        Returns
        =======
        [
            <OpenCongress Bill object>
        ]
        
        """
        return calls.MostOpposedBillsThisWeek(self.key).results
    
    def users_supporting_bills_are_also(self, bill_id, *args, **kwargs):
        """
        Returns bills, people, and issues that are approved or disapproved by 
        OpenCongress users who support the bill indicated by bill_id.
        
        Arguments
        =========
        bill_id = An string specifying a bill's OpenCongress ID
        
        Usage
        =====
        >>> api.users_supporting_bills_are_also('111-h3962')
        
        Returns
        =======
        {
            'also_approved_representatives': [
                <OpenCongress Person object>
            ],
            'also_approved_senators': [
                <OpenCongress Person object>
            ],
            'also_disapproved_representatives': [
                <OpenCongress Person object>
            ],
            'also_disapproved_senators': [
                <OpenCongress Person object>
            ],
            'also_opposing_bills': [
                <OpenCongress Bill object>
            ],
            'also_supporting_bills': [
                <OpenCongress Bill object>
            ],
            'bill': <OpenCongress Bill object (bill_id)>,
            'person': <OpenCongress Person object (bill_id)>,
            'tracking_bills': [
                <OpenCongress Bill object>
            ],
            'tracking_issues': [
                <OpenCongress Issue object>
            ],
            'tracking_people': [
                <OpenCongress Person object>
            ],
            'users_opposing': 40,
            'users_supporting': 76,
        }
        
        """
        return calls.UsersSupportingBillAreAlso(self.key, bill_id, *args, \
            **kwargs).results
    
    def users_tracking_bills_are_also_tracking(self, bill_id, *args, **kwargs):
        """
        Returns bills, people, and issues that are approved or disapproved by 
        OpenCongress users who track the bill indicated by bill_id.
        
        Arguments
        =========
        bill_id = An string specifying a bill's OpenCongress ID
        
        Usage
        =====
        >>> api.users_tracking_bills_are_also_tracking('111-h3962')
        
        Returns
        =======
        {
            'also_approved_representatives': [
                <OpenCongress Person object>
            ],
            'also_approved_senators': [
                <OpenCongress Person object>
            ],
            'also_disapproved_representatives': [
                <OpenCongress Person object>
            ],
            'also_disapproved_senators': [
                <OpenCongress Person object>
            ],
            'also_opposing_bills': [
                <OpenCongress Bill object>
            ],
            'also_supporting_bills': [
                <OpenCongress Bill object>
            ],
            'bill': <OpenCongress Bill object (bill_id)>,
            'person': <OpenCongress Person object (bill_id)>,
            'tracking_bills': [
                <OpenCongress Bill object>
            ],
            'tracking_issues': [
                <OpenCongress Issue object>
            ],
            'tracking_people': [
                <OpenCongress Person object>
            ],
            'users_opposing': 40,
            'users_supporting': 76,
        }
        
        """
        return calls.UsersTrackingBillAreAlsoTracking(self.key, bill_id, \
            *args, **kwargs).results
    
    def issues(self, keyword, *args, **kwargs):
        """
        Queries OpenCongress.org's database of bills matching the passed query
        
        Arguments
        =========
        keyword = A string to search by
        
        Usage
        =====
        >>> api.issues('poverty')
        
        Returns
        =======
        [
            <OpenCongress Issue object>...
        ]
        
        """
        kwargs['keyword'] = keyword
        return calls.Issues(self.key, keyword, *args, **kwargs).results
    
    def battle_royale(self, search_type, *args, **kwargs):
        """
        Queries OpenCongress.org's database for people, issues, or bills based
        on the query. Simulate at http://www.opencongress.org/battle_royale
        
        Usage
        =====
        >>> api.battle_royale('bills', page=1, timeframe='1day')
        
        Returns
        =======
        [
            <OpenCongress (search_type) object>...
        ]
        
        Arguments
        =========
        search_type = A string specifying what you would like to search.
            Possible values: 'bills', 'senators', 'representatives', 
            'issues'
        
        Keyword arguments
        =================
        timeframe = A string specifying the timeframe to search. Possible
            values: '1day', '5days', '30days', '1year'
        page = An integer specifying the page number
        order = A string specifying the sort order. Possible values: 'asc',
            'desc'
        sort = A string specifying the sort criteria. Possible values depend on
            the value of the search_type argument. All search_types are allowed
            to specify 'bookmark_count_1' (total number of users tracking) or
            'total_comments' (total number of user comments). Additionally:
            
            Additional possible values:
                bills: 'vote_count_1' (number of user votes), 
                    'current_support_pb' (number of user votes supporting)
                senators: 'p_approval_count' (number of user votes),
                    p_approval_avg' (average approval rating)
                representatives: 'p_approval_count' (number of user votes),
                    p_approval_avg' (average approval rating)
        
        """
        return calls.BattleRoyale(self.key, search_type, *args, \
            **kwargs).results