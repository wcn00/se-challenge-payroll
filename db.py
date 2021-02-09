import sqlite3
import os
from entry import sheet
import json
from entry import entry

class timesheet:
    ''' 
    timesheet class is responsible for serializing and deserializing sheets and reports
    ''' 
    
    def __init__(self,dbname):
        '''
        Initialize a sqlite database based on the provided filename or open it if it already exists.
        '''
        if os.path.exists(dbname):
            self.conn = sqlite3.connect(dbname)
        else:
            self.conn = sqlite3.connect(dbname)
            self.create_db()

    def __del__(self):
        '''
        Destructor closes the sqlite database if it is open
        '''
        if self.conn != None:
            self.conn.close()

    def create_db(self):        
        '''
        Create the datbase tables in the event that the database is new
        '''
        self.conn.execute('CREATE TABLE timesheet (id INTEGER PRIMARY KEY, work_date DATE NOT NULL, hrs_worked INT NOT NULL, employee_id TEXT NOT NULL, job_group TEXT NOT NULL)')
        self.conn.execute('CREATE TABLE report_id (id INTEGER PRIMARY KEY, report_id TEXT NOT NULL)')
        self.conn.commit()
        
    def add_timesheet(self,rpt_data:sheet):
        '''
        Process the contents of a timesheet file into the database.  Duplicate files are rejected
        '''
        csr = self.conn.cursor()
        csr.execute('SELECT report_id FROM report_id WHERE report_id = ?',[rpt_data.sheet_name])
        if not csr.fetchone() == None:
            raise Exception("Timesheet data {} already processed".format(rpt_data.sheet_name))
        for entry in rpt_data.entry_list:
            csr = csr.execute('INSERT INTO timesheet(work_date,hrs_worked,employee_id,job_group) VALUES (?, ?, ?, ?)',[entry.date,entry.hrs_worked,entry.employee_id,entry.job_group])
        csr = csr.execute('INSERT INTO report_id(report_id) VALUES(?)',[rpt_data.sheet_name])
        self.conn.commit()

    def get_timesheet_report(self):
        '''
        Get a json encoded report of the employee payment database sorted by pay period start date and employee id
        '''            
        csr = self.conn.cursor()
        csr.execute("SELECT work_date, \
            strftime('%Y-%m-',work_date)  || CASE WHEN cast(strftime('%d',work_date) as int) < 16 THEN '01' ELSE '16' END as  pay_period_start  , \
            CASE WHEN cast(strftime('%d',work_date) as int) < 16 THEN date(work_date,'start of month','+14 days') ELSE  date(work_date,'start of month','+1 month','-1 day') END as  pay_period_end  ,\
                sum(hrs_worked) as pay_period_hrs_worked , employee_id,job_group from timesheet group by employee_id,pay_period_start order by pay_period_start asc,employee_id asc")
        rows = csr.fetchall()
        repoemployee_reports  = list()
        for row in rows:
            reportline = {"employeeId":row[4], "payPeriod":{"startDate":row[1],"endDate":row[2]}, "amountPaid":"${:.2f}".format(row[3] * entry.pay_rates[row[5]])}
            repoemployee_reports.append(reportline)
        sorted(repoemployee_reports, key=lambda x: (x['employeeId'],x['payPeriod']['startDate']),reverse=True)       #.sort(key=self.get_start_date).sort(key=get_start_date)
        payroll_report = {"payrollReport":repoemployee_reports}
        return json.dumps(payroll_report)
    

if __name__ == '__main__':
    database = timesheet('timesheet.db')
    cursor = database.conn.execute('SELECT * FROM timesheet')
    
    