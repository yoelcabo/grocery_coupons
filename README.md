# Introduction
This small python program is intended to help you keep track of specific promotion codes from a grocery store.

# Usage

```
usage: monopoly.py [-h] [--check-prizes] [--initialize-db]
                   [--insert-code INSERT_CODE] [--contributor CONTRIBUTOR]
                   [--merge-database MERGE_DATABASE]

Win things with safeway Monopoly.

optional arguments:
  -h, --help            show this help message and exit
  --check-prizes, -p    Shows a balance of the number of codes collected and
                        whether we have any prize won. To be implemented:
                        check by contributor
  --initialize-db       Initializes the db
  --insert-code INSERT_CODE, -i INSERT_CODE
                        Inserts the given code. Optionally you can add your
                        name using the -c option.
  --contributor CONTRIBUTOR, -c CONTRIBUTOR
  --merge-database MERGE_DATABASE, -m MERGE_DATABASE
                        Merge the codes from the given database file.
```

## Getting started

To start using it, just initialize the database and add some codes.
Example:

```
python monopoly.py --initialize-db
python monopoly.py --insert-code 8Y15G --contributor Yoel
```

Then you can simply check your 'balance' of codes collected:

```
$ python monopoly.py --check-prizes
Checking if you guys won some prize...
Group 8Y: 1/8
```

## Sharing information
If you want to share information with your roomate, just interchange the `monopoly.db` file and run `python monopoly --merge-database < db_file >` 

## Inserting multiple codes at once
If you want to insert multiple codes at once, you can use the insert_tickets.sh script, which will prompt you for an owner and then as many codes as you want to add. Do not forget to `--initialize-db` first.
