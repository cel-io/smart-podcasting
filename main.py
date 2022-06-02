import time

from CalculatorAgent import CalculatorAgent
from ClientAgent import ClientAgent
from SumAgent import SumAgent
from config import SERVER

if __name__ == "__main__":

    sum = SumAgent(jid="sumagent" + SERVER, password="password")
    future_sum = sum.start()
    future_sum.result()

    calculator = CalculatorAgent(jid="calculatoragent" + SERVER, password="password")
    future_calculator = calculator.start()
    future_calculator.result()

    client = ClientAgent(op1=1.0, op2=2.0, jid="c1" + SERVER, password="password")
    future_client = client.start()
    future_client.result()

    try:
        while sum.is_alive() or calculator.is_alive() or client.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    client.stop()
