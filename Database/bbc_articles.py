# -*- coding: utf-8 -*-
import sqlite3
import os

conn = sqlite3.connect('bbcdb.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS Article;
DROP TABLE IF EXISTS Category;

CREATE TABLE Article (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title   TEXT UNIQUE,
    content TEXT,
    category_id INTEGER
);

CREATE TABLE Category (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE
);

INSERT INTO Category(name) VALUES ('business');
INSERT INTO Category(name) VALUES ('entertainment');
INSERT INTO Category(name) VALUES ('politics');
INSERT INTO Category(name) VALUES ('sport');
INSERT INTO Category(name) VALUES ('tech')
''')

cat_dict = {'business':1, 'entertainment':2, 
            'politics':3, 'sport':4, 'tech':5}


floc = input('Enter file location: ')
if len(floc) < 1:
    floc = r'C:\Users\mtayl\Desktop\bbc\articles'

count = 0
for cat in cat_dict:
    curloc = floc + '\\' + cat
    all_files = os.listdir(curloc)
    for file in all_files:
        final_path = curloc + '\\' + file
        with open(final_path) as file:  
            title = file.readline().strip()
            content = file.read().strip()
            cur.execute('''INSERT OR IGNORE INTO Article (title, content, category_id)
                            VALUES (?, ?, ?)''', (title, content, cat_dict[cat]))
        
        count += 1
        if count%50==0:
            conn.commit()
    
conn.commit()
conn.close()

# =============================================================================
# cur.execute("SELECT title FROM Article WHERE category_id=2")
# a = cur.fetchmany(5)
# a = [a[i][0] for i in range(len(a))]
# a
# =============================================================================

