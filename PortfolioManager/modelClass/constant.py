'''
Created on Mar 18, 2017

@author: afunes
'''
class Constant:
    #INTERNAL USE
    CONST_POSITION_DICT = "CONST_POSITION_DICT"
    CONST_OLD_POSITION_DICT = "CONST_OLD_POSITION_DICT"
    CONST_BUY = "BUY"
    CONST_SELL = "SELL"
    CONST_IN  = "IN"
    CONST_OUT = "OUT"
    #MOVEMENT
    CONST_MOVEMENT_OID = 0
    CONST_ASSET_OID = 1
    CONST_MOVEMENT_BUY_SELL = 2
    CONST_MOVEMENT_ACQUISITION_DATE = 3
    CONST_MOVEMENT_QUANTITY = 4
    CONST_MOVEMENT_PRICE = 5
    CONST_MOVEMENT_RATE = 6
    CONST_MOVEMENT_GROSS_AMOUNT = 7
    CONST_MOVEMENT_NET_AMOUNT = 8
    CONST_MOVEMENT_COM_PERCENTAGE = 9
    CONST_MOVEMENT_COM_AMOUNT = 10
    CONST_MOVEMENT_COM_VAT_AMOUNT = 11
    CONST_MOVEMENT_TENOR = 12
    CONST_MOVEMENT_CUSTODY_OID = 13
    CONST_MOVEMENT_MATURITY_DATE = 14
    CONST_MOVEMENT_TAX_AMOUNT = 15
    #HARDCODE
    CONST_IVA_PERCENTAGE = 0.16
    CONST_DEF_EQUITY_COMMISSION_PERCENTAGE = 0.0025
    CONST_DEF_OTHER_COMMISSION_PERCENTAGE = 0
    #GUI - POSITION VIEW
    CONST_COLUMN_POSITION_ASSET_NAME = 0
    CONST_COLUMN_POSITION_QUANTITY = CONST_COLUMN_POSITION_ASSET_NAME + 1
    CONST_COLUMN_POSITION_PPP = CONST_COLUMN_POSITION_QUANTITY + 1
    CONST_COLUMN_POSITION_MARKET_PRICE = 3
    CONST_COLUMN_POSITION_CHANGE_PERCENTAGE = 4
    CONST_COLUMN_POSITION_INVESTED_AMOUNT = 5
    CONST_COLUMN_POSITION_VALUATED_AMOUNT = 6
    CONST_COLUMN_POSITION_TENOR = 7
    CONST_COLUMN_POSITION_MATURITY_DATE = 8
    CONST_COLUMN_POSITION_GROSS_PNL = 9
    CONST_COLUMN_POSITION_NET_PNL = 10
    CONST_COLUMN_POSITION_GROSS_PNL_PERCENTAGE = 11
    CONST_COLUMN_POSITION_GROSS_NET_PERCENTAGE = 12
    CONST_COLUMN_POSITION_REALIZED_PNL = 13
    CONST_COLUMN_POSITION_POSITION_PERCENTAGE = 14
    CONST_COLUMN_POSITION_WEIGHTED_PNL = 15
    CONST_COLUMN_POSITION_HIDDEN_ID = 16
    #GUI - SUMMARY CUSTODY VIEW
    CONST_COLUMN_SUMMARY_CUST_CUSTODY_NAME = 0
    CONST_COLUMN_SUMMARY_CUST_ASSET_TYPE_NAME = 1
    CONST_COLUMN_SUMMARY_CUST_INVESTED_AMOUNT = 2
    CONST_COLUMN_SUMMARY_CUST_VALUATED_AMOUNT = 3
    CONST_COLUMN_SUMMARY_CUST_NET_PNL = 4
    CONST_COLUMN_SUMMARY_CUST_NET_PNL_PERCENTAGE = 5
    CONST_COLUMN_SUMMARY_CUST_REALIZED_PNL = 6
    CONST_COLUMN_SUMMARY_CUST_REALIZED_PNL_PLUS_NET_PNL = 7
    CONST_COLUMN_SUMMARY_CUST_POSITION_PERCENTAGE = 8
    CONST_COLUMN_SUMMARY_CUST_WEIGHTED_PNL = 9
    #GUI - MOVEMENT VIEW
    CONST_COLUMN_MOVEMENT_ASSET_NAME = 0
    CONST_COLUMN_MOVEMENT_BUYSELL = 1
    CONST_COLUMN_MOVEMENT_ACQUISITION_DATE = 2
    CONST_COLUMN_MOVEMENT_QUANTITY = 3
    CONST_COLUMN_MOVEMENT_PRICE = 4
    CONST_COLUMN_MOVEMENT_GROSS_AMOUNT = 5
    CONST_COLUMN_MOVEMENT_NET_AMOUNT = 6
    CONST_COLUMN_MOVEMENT_COMMISSION_PERCENTAGE = 7
    CONST_COLUMN_MOVEMENT_COMMISSION_AMOUNT = 8
    CONST_COLUMN_MOVEMENT_COMMISSION_VAT_AMOUNT = 9
    #GUI - CORPORATE EVENT VIEW
    CONST_COLUMN_CE_CUSTODY_NAME = 0
    CONST_COLUMN_CE_CORP_EVENT_TYPE = 1
    CONST_COLUMN_CE_ASSET_NAME = 2
    CONST_COLUMN_CE_PAYMENT_DATE = 3
    CONST_COLUMN_CE_GROSS_AMOUNT = 4
    CONST_COLUMN_CE_HIDDEN_ID = 5
    #GUI - PNL VIEW
    CONST_COLUMN_PNL_ITEM_NAME = 0
    CONST_COLUMN_PNL_INITIAL_POSITION = 1
    CONST_COLUMN_PNL_FINAL_POSITION = 2
    CONST_COLUMN_PNL_CASH_IN = 3
    CONST_COLUMN_PNL_WEIGHTED_CASH_IN = 4
    CONST_COLUMN_PNL_CASH_OUT = 5
    CONST_COLUMN_PNL_WEIGHTED_CASH_OUT = 6
    CONST_COLUMN_PNL_PNL_AMOUNT = 7
    CONST_COLUMN_PNL_WEIGHTED_PNL_AMOUNT = 8
    CONST_COLUMN_PNL_TIR = 9
    CONST_COLUMN_PNL_WEIGHTED_TIR = 10
    #GUI - REPORT MOVEMENT
    CONST_COLUMN_REPORT_MOVEMENT_EVENT_ID= 0
    CONST_COLUMN_REPORT_MOVEMENT_EVENT_TYPE= CONST_COLUMN_REPORT_MOVEMENT_EVENT_ID + 1
    CONST_COLUMN_REPORT_MOVEMENT_EVENT_SUB_TYPE = CONST_COLUMN_REPORT_MOVEMENT_EVENT_TYPE + 1
    CONST_COLUMN_REPORT_MOVEMENT_EVENT_DIRECTION = CONST_COLUMN_REPORT_MOVEMENT_EVENT_SUB_TYPE + 1
    CONST_COLUMN_REPORT_MOVEMENT_ASSET_NAME = CONST_COLUMN_REPORT_MOVEMENT_EVENT_DIRECTION + 1
    CONST_COLUMN_REPORT_MOVEMENT_EVENT_DATE = CONST_COLUMN_REPORT_MOVEMENT_ASSET_NAME + 1
    CONST_COLUMN_REPORT_MOVEMENT_QUANTITY = CONST_COLUMN_REPORT_MOVEMENT_EVENT_DATE + 1
    CONST_COLUMN_REPORT_MOVEMENT_PRICE = CONST_COLUMN_REPORT_MOVEMENT_QUANTITY + 1
    CONST_COLUMN_REPORT_MOVEMENT_RATE = CONST_COLUMN_REPORT_MOVEMENT_PRICE + 1
    CONST_COLUMN_REPORT_MOVEMENT_GROSS_AMOUNT = CONST_COLUMN_REPORT_MOVEMENT_RATE + 1
    CONST_COLUMN_REPORT_MOVEMENT_NET_AMOUNT = CONST_COLUMN_REPORT_MOVEMENT_GROSS_AMOUNT + 1
    CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_PERCENTAGE = CONST_COLUMN_REPORT_MOVEMENT_NET_AMOUNT + 1
    CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_AMOUNT = CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_PERCENTAGE + 1
    CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_IVA_AMOUNT = CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_AMOUNT + 1
    CONST_COLUMN_REPORT_MOVEMENT_TENOR = CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_IVA_AMOUNT + 1
    CONST_COLUMN_REPORT_MOVEMENT_CUSTODY_NAME = CONST_COLUMN_REPORT_MOVEMENT_TENOR + 1
    CONST_COLUMN_REPORT_MOVEMENT_TAX_ID = CONST_COLUMN_REPORT_MOVEMENT_CUSTODY_NAME + 1
    CONST_COLUMN_REPORT_MOVEMENT_TAX_AMOUNT = CONST_COLUMN_REPORT_MOVEMENT_TAX_ID + 1
    CONST_COLUMN_REPORT_MOVEMENT_COMMENT = CONST_COLUMN_REPORT_MOVEMENT_TAX_AMOUNT + 1
    CONST_COLUMN_REPORT_MOVEMENT_EXTERNAL_ID = CONST_COLUMN_REPORT_MOVEMENT_COMMENT + 1
    
    #GUI - IMPORT MOVEMENT
    CONST_COLUMN_IMPORT_MOVEMENT_EVENT_ID= 0
    CONST_COLUMN_IMPORT_MOVEMENT_EVENT_TYPE= CONST_COLUMN_IMPORT_MOVEMENT_EVENT_ID + 1
    CONST_COLUMN_IMPORT_MOVEMENT_EVENT_SUB_TYPE = CONST_COLUMN_IMPORT_MOVEMENT_EVENT_TYPE + 1
    CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DIRECTION = CONST_COLUMN_IMPORT_MOVEMENT_EVENT_SUB_TYPE + 1
    CONST_COLUMN_IMPORT_MOVEMENT_ASSET_NAME = CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DIRECTION + 1
    CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DATE = CONST_COLUMN_IMPORT_MOVEMENT_ASSET_NAME + 1
    CONST_COLUMN_IMPORT_MOVEMENT_QUANTITY = CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DATE + 1
    CONST_COLUMN_IMPORT_MOVEMENT_PRICE = CONST_COLUMN_IMPORT_MOVEMENT_QUANTITY + 1
    CONST_COLUMN_IMPORT_MOVEMENT_RATE = CONST_COLUMN_IMPORT_MOVEMENT_PRICE + 1
    CONST_COLUMN_IMPORT_MOVEMENT_GROSS_AMOUNT = CONST_COLUMN_IMPORT_MOVEMENT_RATE + 1
    CONST_COLUMN_IMPORT_MOVEMENT_NET_AMOUNT = CONST_COLUMN_IMPORT_MOVEMENT_GROSS_AMOUNT + 1
    CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_PERCENTAGE = CONST_COLUMN_IMPORT_MOVEMENT_NET_AMOUNT + 1
    CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_AMOUNT = CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_PERCENTAGE + 1
    CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_IVA_AMOUNT = CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_AMOUNT + 1
    CONST_COLUMN_IMPORT_MOVEMENT_TENOR = CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_IVA_AMOUNT + 1
    CONST_COLUMN_IMPORT_MOVEMENT_CUSTODY_NAME = CONST_COLUMN_IMPORT_MOVEMENT_TENOR + 1
    CONST_COLUMN_IMPORT_MOVEMENT_TAX_ID = CONST_COLUMN_IMPORT_MOVEMENT_CUSTODY_NAME + 1
    CONST_COLUMN_IMPORT_MOVEMENT_TAX_AMOUNT = CONST_COLUMN_IMPORT_MOVEMENT_TAX_ID + 1
    CONST_COLUMN_IMPORT_MOVEMENT_COMMENT = CONST_COLUMN_IMPORT_MOVEMENT_TAX_AMOUNT + 1
    CONST_COLUMN_IMPORT_MOVEMENT_EXTERNAL_ID = CONST_COLUMN_REPORT_MOVEMENT_COMMENT + 1
    CONST_COLUMN_IMPORT_MOVEMENT_HIDDEN_ID = CONST_COLUMN_IMPORT_MOVEMENT_EXTERNAL_ID + 1


    