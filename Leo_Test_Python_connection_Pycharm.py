from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.contract import *
from ibapi.order import *

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId: TickerId, errorcode: int, errorString: str):
        print("Error= ", reqId, " ", errorcode, " ", errorString)

    def contratDetails(self, reqId: int, contractDetails: ContractDetails):
        print("ContractDetails: ", reqId, " ", contractDetails)

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7496, 100)

    contract = Contract()
    contract.symbol = "GE"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NYSE"

    order = Order()
    order.action = "SELL"
    order.totalQuantity = 1
    order.orderType = "MKT"

    app.reqContractDetails(12, contract)

    #order.faGroup = "Group Equal Quantity"
    #order.faMethod = "EqualQuantity"

    oid = 1
    index = 6

    while oid <= 4:

        order.account = "DU22351" + str(index)

        app.placeOrder(oid, contract, order)

        index += 1

        oid += 1

    app.run()

if __name__ == "__main__":
    main()