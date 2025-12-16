# test_order_system.py
import pytest
from unittest.mock import Mock, MagicMock
from dataclasses import dataclass
from datetime import datetime
from typing import List
import sys
import os

# Add the project directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from order import Order
from order_line import OrderLine
from menu import Menu
from menu_items import MenuItem, FoodItem, DrinkItem
from enums import OrderStatus
from order_system import OrderSystem
from customer import Customer
from bill import Bill
from payment import Payment
from payment_service import PaymentService 

@pytest.fixture
def sample_menu():
    menu = Menu("M1", "Test Menu")
    # Add sample items
    food = FoodItem(id="F1", name="Sandwich", description="Test", price=6.50, 
                   dietaryinfo="Gluten", available=True)
    drink = DrinkItem(id="D1", name="Espresso", description="Test", price=2.50,
                     size="S", ishot=True, available=True)
    menu.add_item(food)
    menu.add_item(drink)
    return menu

@pytest.fixture
def sample_customer():
    return Customer(customerid="C1", fullname="Test User", phone="12345678")

@pytest.fixture
def sample_order(sample_customer, sample_menu):
    system = OrderSystem()
    order = system.create_order(sample_customer)
    espresso = sample_menu.get_item("D1")
    sandwich = sample_menu.get_item("F1")
    order.add_item(espresso, 2)
    order.add_item(sandwich, 1)
    return order, system

class TestOrderSystem:
    """Unit tests for core OrderSystem functionality"""
    
    def test_create_order(self, sample_customer):
        system = OrderSystem()
        order = system.create_order(sample_customer)
        assert order.orderid is not None
        assert order.status == OrderStatus.NEW
        assert order.customer == sample_customer [file:2]

    def test_get_nonexistent_order(self, sample_customer):
        system = OrderSystem()
        system.create_order(sample_customer)
        with pytest.raises(KeyError, match="Order not found"):
            system.get_order("nonexistent") [file:2]

class TestOrder:
    """Comprehensive Order class tests including error cases"""
    
    def test_add_unavailable_item(self, sample_customer, sample_menu):
        system = OrderSystem()
        order = system.create_order(sample_customer)
        unavailable_item = sample_menu.get_item("D1")
        sample_menu.set_availability("D1", False)
        
        with pytest.raises(ValueError, match="Item Espresso is not available"):
            order.add_item(unavailable_item, 1) [file:1]

    def test_add_zero_quantity(self, sample_customer, sample_menu):
        system = OrderSystem()
        order = system.create_order(sample_customer)
        item = sample_menu.get_item("D1")
        
        with pytest.raises(ValueError, match="qty must be > 0"):
            order.add_item(item, 0) [file:1]

    def test_remove_nonexistent_item(self, sample_order):
        order, _ = sample_order
        with pytest.raises(KeyError, match="Item not found"):
            order.remove_item("NONEXISTENT") [file:1]

    def test_empty_order_total(self, sample_customer):
        system = OrderSystem()
        order = system.create_order(sample_customer)
        assert order.calculate_total() == 0.0 [file:1]

    def test_calculate_total(self, sample_order):
        order, _ = sample_order
        assert order.calculate_total() == 15.50  # 2*2.50 + 1*6.50 [file:1]

class TestMenu:
    """Menu operations with error handling"""
    
    def test_get_nonexistent_item(self, sample_menu):
        with pytest.raises(KeyError, match="Menu item not found"):
            sample_menu.get_item("NONEXISTENT") [file:6]

    def test_remove_nonexistent_item(self, sample_menu):
        with pytest.raises(KeyError, match="Menu item not found"):
            sample_menu.remove_item("NONEXISTENT") [file:6]

class TestBill:
    """Bill generation tests including empty order and calculation errors"""
    
    def test_generate_bill_empty_order(self, sample_customer):
        system = OrderSystem()
        empty_order = system.create_order(sample_customer)
        with pytest.raises(ValueError, match="Cannot generate bill for empty order"):
            Bill.generate_from_order(empty_order, "B1", 0.15) [file:9]

    def test_generate_bill_invalid_tax_rate(self, sample_order):
        order, _ = sample_order
        with pytest.raises(ValueError, match="Tax rate must be between 0 and 1"):
            Bill.generate_from_order(order, "B1", 2.0) [file:9]

    def test_bill_totals_correct(self, sample_order):
        order, _ = sample_order
        bill = Bill.generate_from_order(order, "B1", 0.15)
        assert bill.subtotal == 15.50
        assert round(bill.total, 2) == 17.82 [file:9]

class TestPaymentService:
    """Payment processing with error handling"""
    
    def test_payment_zero_amount(self):
        with pytest.raises(ValueError, match="Payment amount must be greater than 0"):
            PaymentService.process_payment(0.0) [file:9]

    def test_payment_negative_amount(self):
        with pytest.raises(ValueError, match="Payment amount must be greater than 0"):
            PaymentService.process_payment(-1.0) [file:9]

def test_order_line_calculation():
    """Test OrderLine total calculations"""
    mock_item = Mock()
    mock_item.price = 5.0
    line = OrderLine(item=mock_item, qty=3)
    assert line.unit_price == 5.0
    assert line.line_total == 15.0 [file:3]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
