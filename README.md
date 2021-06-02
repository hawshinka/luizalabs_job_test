# LuizaLabs Job Test

## Source files responsabilities

### Log Parser (log_parser.py) 

Responsible for all the logic regarding reading the log source file and parsing it's lines to extract needed information.

* **Uses:** Game Control

### Game Control (game_control.py)

Responsible of controlling the matches logic and keeping record of all data harvested and transforming them into relevant matches data.

### Game Api (game_api.py)

Responsible for serving the harvested data as  JSON outputs to specific endpoints (read more below).

* **Uses:** Log Parser
* **Required External Libs:** Flask (pip install flask)

## How-Tos

### ... parse the log file and see it's results

Run the following code:
```
$ python log_parser.py
```

### ... run the API server and see it's results

Run the following code:
```
$ python log_parser.py
```

Go to your web browser and access:

* http://127.0.0.1:5000/

To see the entire parsing result

Or:

* http://127.0.0.1:5000/1

To see the match 1 parsing result (change the number to see more)