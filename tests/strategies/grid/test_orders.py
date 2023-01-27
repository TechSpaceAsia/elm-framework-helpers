from elm_framework_helpers.strategies.grid.orders import compute_grid_prices, compute_grid_prices_skewed
from decimal import Decimal as D


def test_compute_grid_prices():
    result = compute_grid_prices(
        price_decimal_places=3,
        center_price=D('0.42352'),
        gap=D('0.001'),
        order_count=10,
    )

    assert result.grid == [
        D('0.422'),
        D('0.424'),
        D('0.421'),
        D('0.425'),
        D('0.420'),
        D('0.426'),
        D('0.419'),
        D('0.427'),
        D('0.418'),
        D('0.428'),
    ]
    assert result.initial == D('0.423')

def test_compute_grid_prices_skewed_towards_bottom():
    result = compute_grid_prices_skewed(
        price_decimal_places=3,
        center_price=D('0.42352'),
        low_price=D('0.416'),
        gap=D('0.001'),
        order_count=10,
    )
    
    assert result.initial == D('0.423')
    assert result.grid == [
        D('0.422'),
        D('0.424'),
        D('0.421'),
        D('0.425'),
        D('0.420'),
        D('0.426'),
        D('0.419'),
        D('0.418'),
        D('0.417'),
        D('0.416'),
    ]