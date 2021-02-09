# Wave Software Development Challenge Run Instructions

This solution is written in python, which is not my best language, but you have to take opportunities to learn when they present themselves.  To run the web server (which is a flask implementatio) simply:  
Unpack the archive, or clone https://github.com/wvchallenges/se-challenge-payroll  
cd se-challenge-payroll/  
source wave/bin/activate  

python3 app.py  
It will open port 8099 on localhost.  
There is a test page at http://localhost:8099  
From there you can upload csv files like the one included in this repo when I forked it.  

There are rest API's at:  
http://localhost:8099/v1/upload   POST Which accepts an uploaded file, tested with Postman  
http://localhost:8099/v1/report   GET  Which will return a report based on all the data in the   database  

To run unit tests:
python3 -m unittest unit_test.py

## Production tweeks
-add security (HTTPS)  
-more unit tests and check coverage  
-compare the generated report to a "gold standard" report in unit tests  
-harden up the error detection, validation and recovery   
-add logging  

## Compromises due to time   
-all the things above :)  
-didn't create new or novel data for testing, just used the provided data.  
-I was going to do a golang implementation as well as python but ran out of time.  