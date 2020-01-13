from datetime import date, datetime

from base.initializer import Initializer
from engine.positionEngine import PositionEngine


def main():
    import logging
    logging.basicConfig(level=logging.INFO)
    Initializer()
    PositionEngine().refreshAll(datetime(2001, 7, 14).date(), datetime.now().date())

if __name__== '__main__':
    main()