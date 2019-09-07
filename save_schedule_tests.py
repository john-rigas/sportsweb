import unittest
import save_schedule
import pickle
from bs4 import BeautifulSoup
import warnings


class SaveScheduleTest(unittest.TestCase):
    
    def test_load_espn_nfl_scores_page(self):
        warnings.filterwarnings('ignore', category=ResourceWarning)
        page_source = save_schedule.load_nfl_scores_page()
        self.assertIn('Weekly League Schedule', page_source)
        self.assertIn('NFL', page_source)

    def test_loading_games_into_list(self):
        with open('nfl_scores_page_source.pl', 'rb') as file:
            page_source = pickle.load(file)
        schedule = save_schedule.get_schedule_and_results_from_html(page_source)
        self.assertIn({'away_team': 'Tampa Bay Buccaneers',
                        'home_team': 'Carolina Panthers',
                        'away_score': '',
                        'home_score': ''}, schedule[2])
        self.assertIn({'away_team': 'Los Angeles Chargers',
                'home_team': 'Miami Dolphins',
                'away_score': '',
                'home_score': ''}, schedule[4])

if __name__ == '__main__':
    unittest.main()