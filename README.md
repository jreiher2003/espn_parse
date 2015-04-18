This project is about parsing all NBA scores from ESPN.com.  
It performs gaussian MLE analysis on the upper and lower bound for 
game match up totals, and also team totals.
If the upper or lower bound number is realized and that number
happens to be the total your bookie gives you then you should know
which way to play.  This works for team totals as well as game totals.

Technology stack is python, BS, MongoDB, scipy, and numpy.  

NOTE: you need to clear out the db.nba database every time you 
run nba_parse_espn.py

before your run nba_parse_espn.py
go to mongo shell - db.nba.drop()
then you can run nba_parse_espn.py
make the daily matchups in nba_analysis.py 
and run it