from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.contract import *
import datetime
import threading
import time
import queue
import array

RUN_FLAG = True
timeout=10
FINISHED = object()
STARTED = object()
TIME_OUT = object()

class finishableQueue(object):

    def __init__(self, queue_to_finish):

        self._queue = queue_to_finish
        self.status = STARTED

    def get(self, timeout):

        contents_of_queue=[]
        finished = False

        while not finished:
            try:
                current_element = self._queue.get(timeout=timeout)
                if current_element is FINISHED:
                    finished = True
                    self.status = FINISHED
                else:
                    contents_of_queue.append(current_element)

            except queue.Empty:
                finished = True
                self.status = TIME_OUT

        return contents_of_queue

    def timed_out(self):
        return self.status is TIME_OUT

class TestWrapper(EWrapper):
    def __init__(self):
        self._my_contract_details = {}
        self._my_historic_data_dict = {}

    def init_error(self):
        error_queue=queue.Queue()
        self._my_errors = error_queue

    def get_error(self, timeout = 5):
        if self.is_error():
            try:
                return self._my_errors.get(timeout=timeout)
            except queue.Empty:
                return None

        return None

    def is_error(self):
        an_error_if = not self._my_errors.empty()
        return an_error_if

    def error(self, reqId: TickerId, errorcode: int, errorString: str):
        print("Error= ", reqId, " ", errorcode, " ", errorString)

    def contratDetails(self, reqId: int, contractDetails: ContractDetails):
        print("ContractDetails: ", reqId, " ", contractDetails)

    def init_historicprices(self, tickerid):
        historic_data_queue = self._my_historic_data_dict[tickerid] = queue.Queue()
        return historic_data_queue

    def historicalData(self, tickerid, bar):
        historic_data_dict = self._my_historic_data_dict
        bardata = (bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume)
        historic_data_dict[tickerid].put(bardata)

    def historicalDataEnd(self, tickerid, start: str, end: str):
        global RUN_FLAG
        RUN_FLAG = False
        if tickerid not in self._my_historic_data_dict.keys():
            self.init_historicprices(tickerid)
        self._my_historic_data_dict[tickerid].put(FINISHED)

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ", reqId, " Date:", bar.date, "Open:", bar.open,
              "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
              "Count:", bar.barCount, "WAP:", bar.average)

    def connectAck(self):
        global RUN_FLAG
        print("Connect ACK")
        RUN_FLAG = True

    def nextValidId(self, orderId: int):
        self.nextOrderId = orderId
        print("I have nextValidId", orderId)

class TestApp(EClient,TestWrapper):
    def __init__(self,TestWrapper):
        EClient.__init__(self,TestWrapper)

    def get_IB_historical_data(self, ib_contract):
        print("Getting historical data from the server... ")
        historic_data_queue = finishableQueue(self.init_historicprices(4101))
        queryTime=(datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
        self.reqHistoricalData(4101, ib_contract, queryTime, "1 Y", "1 day", "MIDPOINT", 1, 1, False, [])
        MAX_WAIT_SECONDS = 10
        historic_data = historic_data_queue.get(timeout = MAX_WAIT_SECONDS)

        while self.wrapper.is_error():
            print(self.get_error())

        if historic_data_queue.timed_out():
            print("Exceeded maximum wait for wrapper to confirm finished - seems to be normal behaviour")

        self.cancelHistoricalData(4101)
        return historic_data

def main():
    global RUN_FLAG
    global index
    client = TestApp(TestWrapper)
    client.connect("127.0.0.1", 7496, 100)
    print("connected")

    threading.Thread(name="TWSAPI_worker", target=client.run).start()

    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.exchange = "IDEALPRO"
    contract.currency = "USD"

    while RUN_FLAG:
        time.sleep(1)
        print("Sleeping...")

    historical_data = client.get_IB_historical_data(contract)
    print(historical_data)
    client.disconnect()
    print("All done")

if __name__ == "__main__":
    main()