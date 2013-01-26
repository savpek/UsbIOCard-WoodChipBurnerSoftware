# coding=utf-8
from datetime import date
import threading
import time
import sqlite3

class StatisticsProcess(threading.Thread):
    DelayBetweenMeasurements = 60 # In seconds.

    _dataBase = None
    _burnerProcess = None

    def __init__(self, burnerProcess):
        self._burnerProcess = burnerProcess
        self._dataBase = sqlite3.connect('statistics.db')

    def run(self):
        while True:
            try:
                time.sleep(self.DelayBetweenMeasurements)
                self._database.execute('''insert into statistics (?,?,?,?)''', [date.today(),
                                                                                self._burnerProcess.ScrewSec,
                                                                                self._burnerProcess.DelaySec,
                                                                                self._burnerProcess.get_fire_value()])
            except Exception:
                pass

    def get_results(self, begin_date, end_date):
        results = []
        for row in self._dataBase.execute('select * from statistics where time < ? and time > ?', [end_date, begin_date]):
            results.append(dict(time=row.time, delay=row.delay, screw=row.screw, fire=row.fire))
        return results