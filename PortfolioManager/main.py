from datetime import date, datetime

from base.initializer import Initializer
from engine.positionEngine import PositionEngine
from core.cache import MainCache


def main():
    import logging
    logging.basicConfig(level=logging.INFO)
    Initializer()
    MainCache.refreshReferenceData()
    PositionEngine().refreshPositions(datetime(2001, 7, 14).date(), datetime.now().date())

if __name__== '__main__':
    main()