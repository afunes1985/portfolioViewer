from datetime import date, datetime
import sys


from core.cache import Singleton
from core.mainEngine import MainEngine


def main():
    import logging
    logging.basicConfig(level=logging.INFO)
    mainEngine.refreshAll(datetime(2001, 7, 14).date(), datetime.now().date())

if __name__== '__main__':
    main()