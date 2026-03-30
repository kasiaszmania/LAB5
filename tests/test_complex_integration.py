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


from src.manager import Manager
from src.models import Parameters
from src.models import Bill


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0

def test_invalid_month_raises_error():
    manager = LocalManager(SimpleParams())
    manager.apartments = {'A1': 'Mieszkanie 1'}
    
   
    with pytest.raises(ValueError):
        manager.get_apartment_costs('A1', 2024, 13)

class SimpleTenant:
    def __init__(self, name, apartment):
        self.name = name
        self.apartment = apartment

def test_create_tenant_settlements():
    manager = LocalManager(SimpleParams())
    manager.apartments = {'A1': 'M1', 'A2': 'M2', 'A3': 'M3'}
    
    t1 = SimpleTenant('Jan', 'A1')
    t2 = SimpleTenant('Anna', 'A1')
    t3 = SimpleTenant('Marek', 'A2')
    manager.tenants = {1: t1, 2: t2, 3: t3}
    
    manager.bills = [
        SimpleBill('A1', 2024, 3, 400.0),
        SimpleBill('A2', 2024, 3, 100.0)
    ]

    res1 = manager.create_tenant_settlements('A1', 2024, 3)
    assert len(res1) == 2
    assert res1[0].tenant == 'Jan'
    assert res1[0].balance_pln == -200.0
    assert res1[1].tenant == 'Anna'
    assert res1[1].balance_pln == -200.0

    res2 = manager.create_tenant_settlements('A2', 2024, 3)
    assert len(res2) == 1
    assert res2[0].tenant == 'Marek'
    assert res2[0].balance_pln == -100.0

    res3 = manager.create_tenant_settlements('A3', 2024, 3)
    assert res3 == []