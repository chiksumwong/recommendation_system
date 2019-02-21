Python: 3.6

```sh
$ pip install numpy
$ pip install pandas
$ pip install scikit-surprise
```

Run Recommendation System

```sh
$ cd <project path>
$ python main.py
```

Leave Recommendation System

```sh
Ctrl + C
```

Put the user preference file and recommendation request file to input folder

User preference file: 
- Filename: UPyyyymmddhhmmss.csv
- yyyymmddhhmmss is the timestamp of the request
- The file contains three columns in a row separated by commas, (userID, itemID, score [1.0-5.0])

Recommendation request file:
- Filename: RRyyyymmddhhmmss.csv
- yyyymmddhhmmss is the timestamp of the request
- The file contains one row with one column (userID)