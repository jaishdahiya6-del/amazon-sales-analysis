import unittest
import pandas as pd
from recommender_engine import NetflixRecommender

class TestRecommender(unittest.TestCase):
    def setUp(self):
        # Create a tiny mock dataset for testing
        data = {
            'title': ['Movie A', 'Movie B', 'Movie C'],
            'description': ['Action in space', 'Space wars', 'Romantic comedy'],
            'listed_in': ['Action', 'Action', 'Romance'],
            'cast': ['John', 'John', 'Jane']
        }
        self.df = pd.DataFrame(data)
        self.engine = NetflixRecommender(self.df)

    def test_recommendation_logic(self):
        # Movie A and B both have 'Space', so they should be similar
        recommendation = self.engine.recommend('Movie A', top_n=1)
        self.assertEqual(recommendation[0], 'Movie B')

if __name__ == '__main__':
    unittest.main()
    import unittest
import pandas as pd
from recommender_engine import NetflixRecommender

class TestRecommender(unittest.TestCase):
    def setUp(self):
        # Create a tiny mock dataset for testing
        data = {
            'title': ['Movie A', 'Movie B', 'Movie C'],
            'description': ['Action in space', 'Space wars', 'Romantic comedy'],
            'listed_in': ['Action', 'Action', 'Romance'],
            'cast': ['John', 'John', 'Jane']
        }
        self.df = pd.DataFrame(data)
        self.engine = NetflixRecommender(self.df)

    def test_recommendation_logic(self):
        # Movie A and B both have 'Space', so they should be similar
        recommendation = self.engine.recommend('Movie A', top_n=1)
        self.assertEqual(recommendation[0], 'Movie B')

if __name__ == '__main__':
    unittest.main()
