import pickle

username = 'johnny'

picks = [
    ('Oakland Raiders', 'Denver Broncos', 'Oakland Raiders'),
    ('New Orleans Saints', 'Houston Texans', 'New Orleans Saints'),
    ('Chicago Bears', 'Green Bay Packers', 'Green Bay Packers'),
    ('New York Jets', 'Buffalo Bills', 'Buffalo Bills'),
    ('Minnesota Vikings', 'Atlanta Falcons', 'Atlanta Falcons'),
    ('Cleveland Browns', 'Tennessee Titans', 'Tennessee Titans'),
    ('Miami Dolphins', 'Baltimore Ravens', 'Baltimore Ravens'),
    ('Philadelphia Eagles', 'Washington Redskins', 'Philadelphia Eagles'),
    ('Carolina Panthers', 'Los Angeles Rams', 'Los Angeles Rams'),
    ('Jacksonville Jaguars', 'Kansas City Chiefs', 'Kansas City Chiefs'),
    ('Los Angeles Chargers', 'Indianapolis Colts', 'Los Angeles Chargers'),
    ('Seattle Seahawks', 'Cincinatti Bengals', 'Seattle Seahawks'),
    ('Dallas Cowboys', 'New York Giants', 'New York Giants'),
    ('Arizona Cardinals', 'Detroit Lions', 'Detroit Lions'),
    ('Tampa Bay Buccaneers', 'San Francisco 49ers', 'San Francisco 49ers'),
    ('New England Patriots', 'Pittsburgh Steelers', 'New England Patriots')
]

selections = [(username, pick[0], pick[1], pick[2]) for pick in picks]

with open('manualpicks.pl', 'wb') as f:
    pickle.dump(selections, f)