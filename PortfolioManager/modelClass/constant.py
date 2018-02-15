'''
Created on Mar 18, 2017

@author: afunes
'''
class Constant:
    CONST_MOVEMENT_OID = 0
    CONST_ASSET_TYPE = 1
    CONST_ASSET_NAME = 2
    CONST_MOVEMENT_BUY_SELL = 3
    CONST_MOVEMENT_ACQUISITION_DATE = 4
    CONST_MOVEMENT_QUANTITY = 5
    CONST_MOVEMENT_PRICE = 6
    CONST_MOVEMENT_RATE = 7
    CONST_MOVEMENT_GROSS_AMOUNT = 8
    CONST_MOVEMENT_NET_AMOUNT = 9
    CONST_MOVEMENT_COM_PERCENTAGE = 10
    CONST_MOVEMENT_COM_AMOUNT = 11
    CONST_MOVEMENT_COM_VAT_AMOUNT = 12
    CONST_MOVEMENT_TENOR = 13
    CONST_MOVEMENT_CUSTODY_OID = 14
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
    CONST_COLUMN_SUMMARY_CUST_SUBTOTAL_NET_PNL = 4
    CONST_COLUMN_SUMMARY_CUST_NET_PNL_PERCENTAGE = 5
    CONST_COLUMN_SUMMARY_CUST_REALIZED_PNL = 6
    CONST_COLUMN_SUMMARY_CUST_POSITION_PERCENTAGE = 7
    CONST_COLUMN_SUMMARY_CUST_WEIGHTED_PNL = 8
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
    CONST_COLUMN_PNL_INITIAL_POSITION = 0
    CONST_COLUMN_PNL_FINAL_POSITION = 1
    CONST_COLUMN_PNL_CASH_IN = 2
    CONST_COLUMN_PNL_WEIGHTED_CASH_IN = 3
    CONST_COLUMN_PNL_CASH_OUT = 4
    CONST_COLUMN_PNL_WEIGHTED_CASH_OUT = 5
    CONST_COLUMN_PNL_PNL_AMOUNT = 6
    CONST_COLUMN_PNL_WEIGHTED_PNL_AMOUNT = 7
    CONST_COLUMN_PNL_TIR = 8
    CONST_COLUMN_PNL_WEIGHTED_TIR = 9

    