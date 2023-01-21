from dataclasses import dataclass
from decimal import Decimal
import decimal


@dataclass
class Grid:
    buy_orders: list[tuple[Decimal, Decimal]]
    sell_orders: list[tuple[Decimal, Decimal]]


def compute_grid_orders(
    bid_price: Decimal,
    ask_price: Decimal,
    amount_per_order: Decimal,
    gap: Decimal,
    order_count: int,
    quantity_decimal_places: int,
) -> Grid:
    buy_orders = []
    sell_orders = []
    with decimal.localcontext() as context:
        context.rounding = decimal.ROUND_DOWN
        for i in range(order_count):
            price = bid_price - i * gap
            quantity = round(amount_per_order / price, quantity_decimal_places)
            buy_orders.append((price, quantity))
            sell_orders.append((ask_price + i * gap, quantity))

    return Grid(buy_orders=buy_orders, sell_orders=sell_orders)
