import pytest
from src.manager import Manager

class SimpleParams:
    pass

class LocalManager(Manager):
    def load_data(self):
        pass

class SimpleBill:
    def __init__(self, apartment, settlement_year, settlement_month, amount_pln):
        self.apartment = apartment
        self.settlement_year = settlement_year
        self.settlement_month = settlement_month
        self.amount_pln = amount_pln

def test_get_apartment_costs():
    manager = LocalManager(SimpleParams())
    
    manager.apartments = {'A1': 'Mieszkanie 1', 'A2': 'Mieszkanie 2'}
    
    manager.bills = [
        SimpleBill('A1', 2024, 3, 200.0),
        SimpleBill('A1', 2024, 3, 250.0),
        SimpleBill('A1', 2024, 4, 100.0),
        SimpleBill('A2', 2024, 3, 300.0)
    ]

    assert manager.get_apartment_costs('A1', 2024, 3) == 450.0
    assert manager.get_apartment_costs('A2', 2024, 4) == 0.0
    assert manager.get_apartment_costs('Z99', 2024, 3) is None