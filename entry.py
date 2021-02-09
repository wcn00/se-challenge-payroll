import datetime
class entry:
    pay_rates = {'A':20,'B':30}
    '''
    entry represents a timesheet work entry
    '''
    def __init__(self,entryString):
        entryList = entryString.split(',')
        entryDate = entryList[0].split('/')
        if len(entryDate) != 3 or not entryDate[2].isdigit() or not entryDate[1].isdigit() or not entryDate[0].isdigit():
            raise Exception("invalid date: {}".format(entryList[0]))
        self.date = datetime.datetime(int(entryDate[2]),int(entryDate[1]),int(entryDate[0]))
        self.hrs_worked = float(entryList[1])
        self.employee_id = int(entryList[2])
        self.job_group = entryList[3].upper()
        

class sheet:
    '''
    sheet represents a list of work entries and the file from which they came
    '''
    def __init__(self,entry_list,sheet_name):
        self.sheet_name = sheet_name
        self.entry_list = entry_list
        
