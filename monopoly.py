import uuid
import sqlite3
import re
import argparse

DB_FILE = "monopoly.db"
def create_database():
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  c.execute('''CREATE TABLE groups (
		  id TEXT PRIMARY KEY,
		  number_of_objects INTEGER
		  ) ''')
  c.execute('''CREATE TABLE codes (
                  internal_id TEXT PRIMARY KEY,
		  code TEXT,
		  group_id TEXT,
		  contributor TEXT,
		  FOREIGN KEY(group_id) REFERENCES groups(id)
		  ) ''')
  conn.commit()
  conn.close()

def insert_group(group_id, number_of_objects):
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  group_id = group_id.upper()
  c.execute("INSERT INTO groups (id, number_of_objects) VALUES ('{}', '{}')".format(group_id,number_of_objects))
  conn.commit()
  conn.close()


def initialize_db():
  print "Initializing database..."
  create_database()
  insert_group('8Y',8)
  insert_group('8Z',8)
  insert_group('8B',5)
  insert_group('8C',5)
  insert_group('8D',5)
  insert_group('8E',5)
  insert_group('9A',5)
  insert_group('9B',5)


def validate_code(code):
  re.compile("^[0-9][A-Za-z][0-9][0-9][A-Za-z]$").match(code)

def createGroupIfDoesntExists(group_id):
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  t = (group_id,)
  c.execute('SELECT * FROM groups WHERE id=?', t)
  if len(c.fetchall()) == 0:
    insert_group(group_id, 4)
  conn.commit()
  conn.close()

def insert_code(code,contributor):
  validate_code(code)
  code = code.upper()
  group_id = code[:2]
  createGroupIfDoesntExists(group_id)
  unique_id = uuid.uuid1()
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  c.execute("INSERT INTO codes (code, group_id, contributor, internal_id) VALUES ('{}', '{}', '{}', '{}')".format(code, group_id, contributor, unique_id))
  conn.commit()
  conn.close()

def check_prizes():
  print 'Checking if you guys won some prize...'
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  for row in c.execute("SELECT group_id, COUNT(DISTINCT code), number_of_objects FROM codes INNER JOIN groups ON codes.group_id = groups.id GROUP BY group_id "):
    print 'Group {}: {}/{}'.format(*row) 
    if row[1] == row[2]:
      print '  CONGRATS, you can get a prize for ' + row[0]
  
  conn.commit()
  conn.close()

def merge_database(db):
  conn = sqlite3.connect(DB_FILE)
  connMg = sqlite3.connect(db)
  c = conn.cursor()
  cMg = connMg.cursor()
  for row in cMg.execute("SELECT * FROM codes"):
    createGroupIfDoesntExists(row[2])
    c.execute("INSERT OR IGNORE INTO codes VALUES (?,?,?,?)",row)
  conn.commit()
  conn.close()
  connMg.close()
  
def main():
  parser = argparse.ArgumentParser(description='Win things with safeway Monopoly.')
  parser.add_argument('--check-prizes', '-p', action='store_true', help='Shows a balance of the number of codes collected and whether we have any prize won. To be implemented: check by contributor')
  parser.add_argument('--initialize-db', action='store_true', help='Initializes the db')
  parser.add_argument('--insert-code', '-i', help='Inserts the given code. Optionally you can add your name using the -c option.')
  parser.add_argument('--contributor', '-c')
  parser.add_argument('--merge-database', '-m', help='Merge the codes from the given database file.')
 
  args = parser.parse_args()
  
  if args.initialize_db:
    initialize_db()
  elif args.insert_code is not None:
    if args.contributor is not None:
      insert_code(args.insert_code,args.contributor)
    else:
      insert_code(args.insert_code, 'default_contributor')
  elif args.merge_database is not None:
    merge_database(args.merge_database) 
  elif args.check_prizes:
    if args.contributor is not None:
      check_prizes(args.contributor)
    else:
      check_prizes()
  else:
    parser.print_help()

if __name__ == "__main__": main()
