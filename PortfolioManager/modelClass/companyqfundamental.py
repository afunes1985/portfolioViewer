'''
Created on 7 ago. 2018

@author: afunes
'''
class CompanyQFundamental():
    def __init__(self, row):
        self.company_id = None
        self.indicator_id = None
        self.q_2011Q2 = None
        self.q_2011Q3 = None
        self.q_2011Q4 = None
        self.q_2012Q1 = None
        self.q_2012Q2 = None 
        self.q_2012Q3 = None
        self.q_2012Q4 = None
        self.q_2013Q1 = None
        self.q_2013Q2 = None
        self.q_2013Q3 = None
        self.q_2013Q4 = None
        self.q_2014Q1 = None
        self.q_2014Q2 = None
        self.q_2014Q3 = None
        self.q_2014Q4 = None
        self.q_2015Q1 = None
        self.q_2015Q2 = None
        self.q_2015Q3 = None
        self.q_2015Q4 = None
        self.q_2016Q1 = None
        self.q_2016Q2 = None
        self.q_2016Q3 = None
        self.q_2016Q4 = None
        self.q_2017Q1 = None
        self.q_2017Q2 = None
        self.q_2017Q3 = None
        self.q_2017Q4 = None
        self.q_2018Q1 = None
        self.q_2018Q2 = None
        if(row is not None):
            self.setAttr(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29])
    
    def setAttr(self, OID, q_company_id, q_indicator_id, q_2011Q2, q_2011Q3, q_2011Q4, q_2012Q1, q_2012Q2, q_2012Q3, q_2012Q4, q_2013Q1, q_2013Q2, q_2013Q3, q_2013Q4, q_2014Q1, q_2014Q2, q_2014Q3, q_2014Q4, q_2015Q1, q_2015Q2, q_2015Q3, q_2015Q4, q_2016Q1, q_2016Q2, q_2016Q3, q_2016Q4, q_2017Q1, q_2017Q2, q_2017Q3, q_2017Q4, q_2018Q1, q_2018Q2):
        self.OID = OID
        self.q_company_id = q_company_id
        self.q_indicator_id = q_indicator_id
        self.q_2011Q2 = q_2011Q2
        self.q_2011Q3 = q_2011Q3
        self.q_2011Q4 = q_2011Q4
        self.q_2012Q1 = q_2012Q1
        self.q_2012Q2 = q_2012Q2 
        self.q_2012Q3 = q_2012Q3
        self.q_2012Q4 = q_2012Q4
        self.q_2013Q1 = q_2013Q1
        self.q_2013Q2 = q_2013Q2
        self.q_2013Q3 = q_2013Q3
        self.q_2013Q4 = q_2013Q4
        self.q_2014Q1 = q_2014Q1
        self.q_2014Q2 = q_2014Q2
        self.q_2014Q3 = q_2014Q3
        self.q_2014Q4 = q_2014Q4
        self.q_2015Q1 = q_2015Q1
        self.q_2015Q2 = q_2015Q2
        self.q_2015Q3 = q_2015Q3
        self.q_2015Q4 = q_2015Q4
        self.q_2016Q1 = q_2016Q1
        self.q_2016Q2 = q_2016Q2
        self.q_2016Q3 = q_2016Q3
        self.q_2016Q4 = q_2016Q4
        self.q_2017Q1 = q_2017Q1
        self.q_2017Q2 = q_2017Q2
        self.q_2017Q3 = q_2017Q3
        self.q_2017Q4 = q_2017Q4
        self.q_2018Q1 = q_2018Q1
        self.q_2018Q2 = q_2018Q2
