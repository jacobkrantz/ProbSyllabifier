from __future__ import print_function

from collections import OrderedDict

dl = data_loader('wordforms_db')
# these commands were run in other locations. Pooled together for history.

# 1st on 6/17
cols_and_types = OrderedDict([
    ('Word', 'TEXT'),
    ('PhonCLX', 'TEXT'),
    ('PhonCPA', 'TEXT'),
    ('PhonDISC', 'TEXT'),
    ('PhonSAM', 'TEXT'),
    ('PronCnt', 'INTEGER')
])
dl.create_table('pronunciations', cols_and_types)
# 2nd on 6/17
cols_and_types = OrderedDict([('Word', 'TEXT'), ('WordCnt', 'INTEGER')])
dl.create_table('words', cols_and_types)
# 3rd on 6/17
cols_and_types = OrderedDict([
    ('Word', 'TEXT'),
    ('PhonSylCLX', 'TEXT'),
    ('PhonSylCPA', 'TEXT'),
    ('PhonSylDISC', 'TEXT'),
    ('PhonSylSAM', 'TEXT'),
    ('SylCnt', 'INTEGER'),
    ('WordSyl', 'TEXT')
])
dl.create_table('syllabifications', cols_and_types)

# -------------------------------

base_dir = 'C:\Users\Jacob\Desktop\wordforms'

# 1-3 ran in data_loader.py
# 1st on 6/18       load the words table
# 2nd on 6/18       load the pronunciations table
# 3rd on 6/18       load the syllabifications table

cols_list = [
    ['Word', 'WordCnt'],
    ['Word', 'PhonCLX', 'PhonCPA', 'PhonDISC', 'PhonSAM', 'PronCnt'],
    ['Word', 'PhonSylCLX', 'PhonSylCPA', 'PhonSylDISC', 'PhonSylSAM',
     'SylCnt', 'WordSyl']
]
tables_list = ['words', 'pronunciations', 'syllabifications']

for cols, table in zip(cols_list, tables_list):
    for i in range(1, 6):
        dl.load_table_from_file(
            table,
            '{}\{}-{}.txt'.format(base_dir, table, i),
            cols
        )
        print('{} done'.format(i))

# -------------------------------

# 6/23
cols_and_types = OrderedDict([
    ('Word', 'TEXT'),
    ('ProbSyl', 'TEXT'),
    ('CSyl', 'TEXT'),
    ('Same', 'INTEGER')
])
dl.create_table('workingresults', cols_and_types)

#--------------------------------

# 11/18 done in DB Browser for SQLite
"""
INSERT INTO optimized_disc (word, pronunciation, syllabification)
SELECT
	syllabifications.Word,
	pronunciations.PhonDISC,
	syllabifications.PhonSylDISC
FROM syllabifications
JOIN pronunciations
	ON syllabifications.Word = pronunciations.Word
""""
