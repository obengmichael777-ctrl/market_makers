import quickfix as fix
import quickfix44 as fix44
import time

class MyMarketMakerApp(fix.Application):
    def __init__(self):
        super().__init__()
        self.session_id = None

    def onCreate(self, sessionID):
        self.session_id = sessionID
        print(f"[SESSION] Created: {sessionID}")

    def onLogon(self, sessionID):
        self.session_id = sessionID
        print("[SESSION] Logged on successfully!")
        self.place_quote()

    def onLogout(self, sessionID):
        print("[SESSION] Logged out.")

    def toApp(self, message, sessionID):
        pass

    def toAdmin(self, message, sessionID):
        pass

    def fromApp(self, message, sessionID):
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        
        if msgType.getValue() == fix.MsgType_ExecutionReport:
            clOrdID = fix.ClOrdID()
            execType = fix.ExecType()
            ordStatus = fix.OrdStatus()
            
            message.getField(clOrdID)
            message.getField(execType)
            message.getField(ordStatus)
            
            print(f"[EXEC REPORT] Order: {clOrdID.getValue()}, Status: {ordStatus.getValue()}")
            
            if execType.getValue() == fix.ExecType_FILL:
                lastQty = fix.LastQty()
                lastPx = fix.LastPx()
                message.getField(lastQty)
                message.getField(lastPx)
                print(f" -> FILL: {lastQty.getValue()} @ {lastPx.getValue()}")

    def place_quote(self):
        self.send_order(fix.Side_BUY, 100, 45.00, "BID_001")
        self.send_order(fix.Side_SELL, 100, 45.50, "ASK_001")

    def send_order(self, side, qty, price, cl_ord_id):
        if not self.session_id:
            return
        order = fix44.NewOrderSingle()
        order.set(fix.ClOrdID(cl_ord_id))
        order.set(fix.Symbol("VOW"))
        order.set(fix.Side(side))
        order.set(fix.OrdType(fix.OrdType_LIMIT))
        order.set(fix.Price(price))
        order.set(fix.OrderQty(qty))
        order.set(fix.TransactTime())
        
        fix.Session.sendToTarget(order, self.session_id)
        print(f"[SENT] {cl_ord_id}: {qty} @ {price}")

def main():
    try:
        settings = fix.SessionSettings("client.cfg")
        application = MyMarketMakerApp()
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        
        initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)
        initiator.start()
        
        while True:
            time.sleep(1)
            
    except (fix.ConfigError, fix.RuntimeError) as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
