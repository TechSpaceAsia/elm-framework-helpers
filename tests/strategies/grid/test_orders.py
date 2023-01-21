from elm_framework_helpers.strategies.grid.orders import compute_grid_orders
from decimal import Decimal as D


def test_compute_grid_orders():
    result = compute_grid_orders(
        bid_price=D(20),
        ask_price=D(21),
        amount_per_order=100,
        gap=2,
        order_count=2,
        quantity_decimal_places=3,
    )

    assert result == [
        (
            (D('18'), D('5.555')), (D('23'), D('5.555')),
        ),
        (
            (D('16'), D('6.25')), (D('25'), D('6.25'))
        ),
    ]

