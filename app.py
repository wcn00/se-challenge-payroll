from flask import Flask,render_template,request,abort
#from werkzeug import secure_filename
from entry import entry,sheet
import db

TS = None
app = Flask(__name__)
'''The default database name'''
DATABASE_NAME='timesheet.db'
@app.route('/')
def root():
    '''
    The root path for this app allows for testing the file upload capability    
    '''
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload_timesheet():
    '''
    The upload route accepts a posted csv file with employee timesheet info, used for testing from the index page
    '''
    global DATABASE_NAME
    global TS
    try:
        csv_data = request.files['file'].read().decode(encoding='utf-8').split('\r\n')
        add_csv_to_database(csv_data)
    except Exception as e:
        return render_template('error.html',message = e)
    return render_template('index.html')

@app.route('/v1/upload',methods=['POST'])
def upload_timesheetv1():
    '''
    The upload route accepts a posted csv file with employee timesheet info
    '''
    global DATABASE_NAME
    global TS
    try:
        csv_data = request.files['file'].read().decode(encoding='utf-8').split('\r\n')
        entrylist = list()
        for line in csv_data[1:]:
            if(len(line)<=0):
                continue
            entrylist.append(entry(line))
        sht = sheet(entrylist,request.files['file'].filename)
        if(TS == None):
            TS = db.timesheet(DATABASE_NAME)
        TS.add_timesheet(sht)
    except Exception as e:
        abort(400,"{}".format(e))
    return "200"

@app.route('/v1/report',methods=['GET'])
def report():
    '''
    The report route retrieves a json formatted employee payment report
    '''
    try:
        global TS
        if TS == None:
            TS = db.timesheet(DATABASE_NAME)
        return TS.get_timesheet_report()
    except Exception as e:
        abort(400,"{}".format(e))

def add_csv_to_database(csv_data):
    global TS  
    entrylist = list()
    for line in csv_data[1:]:
        if(len(line)<=0):
            continue
        entrylist.append(entry(line))
    sht = sheet(entrylist,request.files['file'].filename)
    if(TS == None):
        TS = db.timesheet(DATABASE_NAME)
    TS.add_timesheet(sht)

if __name__ == '__main__':
    app.run('0.0.0.0', 8099,True)
    
    