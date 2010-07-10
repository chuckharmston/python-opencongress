import opencongress, unittest

API_KEY = '2670a003f1dab7cf502b8d39eb2a95639fc6849c'


class Utils(unittest.TestCase):
    
    def test_url_date(self):
        import datetime
        self.assertEqual(
            url_date(datetime.date(2000, 1, 1)),
            'Jan 01st, 2000'
        )
        self.assertEqual(
            url_date(datetime.date(2000, 1, 2)),
            'Jan 02nd, 2000'
        )
        self.assertEqual(
            url_date(datetime.date(2000, 1, 3)),
            'Jan 03rd, 2000'
        )
        self.assertEqual(
            url_date(datetime.date(2000, 1, 4)),
            'Jan 04th, 2000'
        )
        self.assertEqual(
            url_date(datetime.date(2000, 1, 20)),
            'Jan 20th, 2000'
        )
        self.assertEqual(
            url_date(datetime.date(2000, 1, 31)),
            'Jan 31st, 2000'
        )


class ApiMethods(unittest.TestCase):
    
    def setUp(self):
        self.api = opencongress.Api(API_KEY)
    
    def test_api_instance(self):
        self.assertIsInstance(self.api, opencongress.Api)
        
    def test_api_nokey(self):
        def forgottenKey():
            opencongress.Api()
        self.assertRaises(TypeError, forgottenKey)
    
    def test_people(self):
        self.assertIsInstance(
            self.api.people()[0],
            opencongress.classes.Person
        )
    
    def test_people_first_name(self):
        self.assertIsInstance(
            self.api.people(first_name='John')[0],
            opencongress.classes.Person
        )
    
    def test_people_last_name(self):
        self.assertIsInstance(
            self.api.people(last_name='Kerry')[0],
            opencongress.classes.Person
        )
    
    def test_people_person_id(self):
        self.assertIsInstance(
            self.api.people(person_id=300056)[0],
            opencongress.classes.Person
        )
    
    def test_people_gender(self):
        self.assertIsInstance(
            self.api.people(gender='M')[0],
            opencongress.classes.Person
        )
        
        def invalidArgument():
            self.api.people(gender='f')
        
        self.assertRaises(
            opencongress.exceptions.ArgumentError,
            invalidArgument
        )
    
    def test_people_state(self):
        self.assertIsInstance(
            self.api.people(state='AZ')[0],
            opencongress.classes.Person
        )
        
        def invalidArgument():
            self.api.people(state='az')
            
        self.assertRaises(
            opencongress.exceptions.ArgumentError,
            invalidArgument
        )
    
    def test_people_party(self):
        people = self.api.people(party='Republican')
        self.assertIsInstance(people[0], opencongress.classes.Person)
    
    def test_people_party_invalid_argument(self):
        def invalidArgument():
            self.api.people(state='republican')
        self.assertRaises(
            opencongress.exceptions.ArgumentError,
            invalidArgument
        )
    
    def test_people_user_approval(self):
        self.assertIsInstance(
            self.api.people(user_approval=(3, 4,))[0],
            opencongress.classes.Person
        )
    
    def test_people_user_approval_reverse(self):
        self.assertIsInstance(
            self.api.people(user_approval=(4, 3,))[0],
            opencongress.classes.Person
        )
    
    def test_people_compound_search(self):
        people = self.api.people(
            state='MN',
            first_name='Al',
            last_name='Franken',
            party='Democrat'
        )
        self.assertEqual(len(people), 1)
        self.assertIsInstance(people[0], opencongress.classes.Person)
    
    def test_people_senators_most_in_the_news_this_week(self):
        self.assertIsInstance(
            self.api.senators_most_in_the_news_this_week()[0],
            opencongress.classes.Person
        )
    
    def test_representatives_most_in_the_news_this_week(self):
        self.assertIsInstance(
            self.api.representatives_most_in_the_news_this_week()[0],
            opencongress.classes.Person
        )
    
    def test_most_blogged_senators_this_week(self):
        self.assertIsInstance(
            self.api.most_blogged_senators_this_week()[0],
            opencongress.classes.Person
        )
    
    def test_most_blogged_representatives_this_week(self):
        self.assertIsInstance(
            self.api.most_blogged_representatives_this_week()[0],
            opencongress.classes.Person
        )
    
    def test_compare_two_people(self):
        results = self.api.compare_two_people(300001, 300013)
        self.assertIsInstance(results['person1'], opencongress.classes.Person)
        self.assertIsInstance(results['person2'], opencongress.classes.Person)
        self.assertIsInstance(
            results['hot_votes'][0],
            opencongress.classes.Vote
        )
        self.assertIsInstance(
            results['other_votes'][0],
            opencongress.classes.Vote
        )
    
    def test_compare_two_people_invalid_argument(self):
        def invalidArgument():
            self.api.compare_two_people()
        self.assertRaises(TypeError, invalidArgument)
    
    def test_users_supporting_person_are_also(self):
        results = self.api.users_supporting_person_are_also(300060)
        self.assertIsInstance(results['person'], opencongress.classes.Person)
        self.assertIsInstance(
            results['also_approved_representatives'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_approved_senators'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_disapproved_representatives'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_disapproved_senators'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_opposing_bills'][0], 
            opencongress.classes.Bill
        )
        self.assertIsInstance(
            results['also_supporting_bills'][0], 
            opencongress.classes.Bill
        )
    
    def test_users_opposing_person_are_also(self):
        results = self.api.users_opposing_person_are_also(300060)
        self.assertIsInstance(results['person'], opencongress.classes.Person)
        self.assertIsInstance(
            results['also_approved_representatives'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_approved_senators'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_disapproved_representatives'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_disapproved_senators'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_opposing_bills'][0], 
            opencongress.classes.Bill
        )
        self.assertIsInstance(
            results['also_supporting_bills'][0], 
            opencongress.classes.Bill
        )
    
    def test_users_tracking_person_are_also(self):
        results = self.api.users_tracking_person_are_also(300060)
        self.assertIsInstance(results['person'], opencongress.classes.Person)
        self.assertIsInstance(
            results['tracking_people'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['tracking_bills'][0], 
            opencongress.classes.Bill
        )
        self.assertIsInstance(
            results['tracking_issues'][0], 
            opencongress.classes.Issue
        )
    
    def test_bills(self):
        self.assertIsInstance(
            self.api.bills()[0],
            opencongress.classes.Bill
        )

    def test_bills_type(self):
        self.assertIsInstance(
            self.api.bills(type='hj')[0],
            opencongress.classes.Bill
        )
    
    def test_bills_type_invalid(self):
        def invalidArgument():
            self.api.bills(type='zz')
        self.assertRaises(
            opencongress.exceptions.ArgumentError,
            invalidArgument
        )
    
    def test_bills_congress(self):
        self.assertIsInstance(
            self.api.bills(congress=111)[0],
            opencongress.classes.Bill
        )
    
    def test_bills_number(self):
        self.assertIsInstance(
            self.api.bills(number=5749)[0],
            opencongress.classes.Bill
        )
    
    def test_bills_compound(self):
        self.assertIsInstance(
            self.api.bills(type='hj', congress=111)[0],
            opencongress.classes.Bill
        )
    
    def test_bills_by_ident(self):
        results = self.api.bills_by_ident('111-h2454', '111-h3962')
        self.assertIsInstance(results[0], opencongress.classes.Bill)
        self.assertEqual(results[0].id, 57656)
        self.assertIsInstance(results[1], opencongress.classes.Bill)
        self.assertEqual(results[1].id, 60845)
    
    def test_bills_introduced_since(self):
        import datetime
        self.assertIsInstance(
            self.api.bills_introduced_since(datetime.date(2009, 07, 04))[0],
            opencongress.classes.Bill
        )
    
    def test_bills_by_query(self):
        self.assertIsInstance(
            self.api.bills('Global Poverty Act of 2007')[0],
            opencongress.classes.Bill
        )
    
    def test_hot_bills(self):
        self.assertIsInstance(
            self.api.hot_bills()[0],
            opencongress.classes.Bill
        )
    
    def test_most_blogged_bills_this_week(self):
        self.assertIsInstance(
            self.api.most_blogged_bills_this_week()[0],
            opencongress.classes.Bill
        )
    
    def test_bills_in_the_news_this_week(self):
        self.assertIsInstance(
            self.api.bills_in_the_news_this_week()[0],
            opencongress.classes.Bill
        )
    
    def test_most_tracked_bills_this_week(self):
        self.assertIsInstance(
            self.api.most_tracked_bills_this_week()[0],
            opencongress.classes.Bill
        )
    
    def test_most_supported_bills_this_week(self):
        self.assertIsInstance(
            self.api.most_supported_bills_this_week()[0],
            opencongress.classes.Bill
        )
    
    def test_most_opposed_bills_this_week(self):
        self.assertIsInstance(
            self.api.most_opposed_bills_this_week()[0],
            opencongress.classes.Bill
        )
    
    def test_users_supporting_bills_are_also(self):
        results = self.api.users_supporting_bills_are_also('111-h3962')
        self.assertIsInstance(
            results['also_approved_representatives'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_approved_senators'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_disapproved_representatives'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_opposing_bills'][0], 
            opencongress.classes.Bill
        )
        self.assertIsInstance(
            results['also_supporting_bills'][0], 
            opencongress.classes.Bill
        )
        self.assertIsInstance(
            results['bill'], 
            opencongress.classes.Bill
        )
        self.assertIsInstance(
            results['person'], 
            opencongress.classes.Person
        )
    
    def test_users_tracking_bills_are_also_tracking(self):
        results = self.api.users_tracking_bills_are_also_tracking('111-h3962')
        self.assertIsInstance(
            results['also_approved_representatives'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_approved_senators'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_disapproved_representatives'][0], 
            opencongress.classes.Person
        )
        self.assertIsInstance(
            results['also_opposing_bills'][0], 
            opencongress.classes.Bill
        )
        self.assertIsInstance(
            results['also_supporting_bills'][0], 
            opencongress.classes.Bill
        )
        self.assertIsInstance(
            results['bill'], 
            opencongress.classes.Bill
        )
        self.assertIsInstance(
            results['person'], 
            opencongress.classes.Person
        )
    
    def test_issues(self):
        self.assertIsInstance(
            self.api.issues('poverty')[0],
            opencongress.classes.Issue
        )
    
    def test_battle_royale(self):
        self.assertIsInstance(
            self.api.battle_royale('bills')[0],
            opencongress.classes.Bill
        )
        self.assertIsInstance(
            self.api.battle_royale('issues')[0],
            opencongress.classes.Issue
        )
        self.assertIsInstance(
            self.api.battle_royale('senators')[0],
            opencongress.classes.Person
        )
        self.assertIsInstance(
            self.api.battle_royale('representatives')[0],
            opencongress.classes.Person
        )
    
    def test_battle_royale_timeframe(self):
        self.assertIsInstance(
            self.api.battle_royale('bills', timeframe='1day')[0],
            opencongress.classes.Bill
        )
        
        def invalidArgument():
            self.api.battle_royale('bills', timeframe='0day')[0],
        self.assertRaises(
            opencongress.exceptions.ArgumentError,
            invalidArgument
        )
    
    def test_battle_royale_page(self):
        self.assertIsInstance(
            self.api.battle_royale('bills', page=2)[0],
            opencongress.classes.Bill
        )
    
    def test_battle_royale_order(self):
        self.assertIsInstance(
            self.api.battle_royale('bills', order='asc')[0],
            opencongress.classes.Bill
        )
        
        def invalidArgument():
            self.api.battle_royale('bills', order='ascdesc')[0],
        self.assertRaises(
            opencongress.exceptions.ArgumentError,
            invalidArgument
        )
    
    def test_battle_royale_sort(self):
        self.assertIsInstance(
            self.api.battle_royale('senators', sort='total_comments')[0],
            opencongress.classes.Person
        )
        
        def invalidArgument():
            self.api.battle_royale('senators', sort='doh')[0],
        self.assertRaises(
            opencongress.exceptions.ArgumentError,
            invalidArgument
        )
        
        self.assertIsInstance(
            self.api.battle_royale('issues', sort='total_comments')[0],
            opencongress.classes.Issue
        )
        
        def invalidArgument():
            self.api.battle_royale('issues', sort='doh')[0],
        self.assertRaises(
            opencongress.exceptions.ArgumentError,
            invalidArgument
        )
        
        self.assertIsInstance(
            self.api.battle_royale('bills', sort='total_comments')[0],
            opencongress.classes.Bill
        )
        
        def invalidArgument():
            self.api.battle_royale('bills', sort='doh')[0],
        self.assertRaises(
            opencongress.exceptions.ArgumentError,
            invalidArgument
        )


if __name__ == '__main__':
    unittest.main()