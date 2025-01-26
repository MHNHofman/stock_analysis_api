from src.screener.stock_metrics_constraints import StockScreenerConstraints


class TestStockScreenerConstraints:

    def test_set_constraints_undervalued(self) -> None:
        """
        Function to test the methods to set constraints
        :return: None
        """
        stock_screener_constraints = StockScreenerConstraints
        undervalued_metrics_constraints = (
            stock_screener_constraints.set_constraints_undervalued_stocks()
        )
        assert type(undervalued_metrics_constraints) == tuple
        assert len(undervalued_metrics_constraints) == 2
        assert undervalued_metrics_constraints[0]['screener'] == 'undervalued'


    def test_set_constraints_growth(self) -> None:
        """
        Function to test the methods to set constraints
        :return: None
        """
        stock_screener_constraints = StockScreenerConstraints
        growth_metrics_constraints = stock_screener_constraints.set_constraints_growth_stocks()
        assert type(growth_metrics_constraints) == tuple
        assert len(growth_metrics_constraints) == 2
        assert growth_metrics_constraints[0]['screener'] == 'growth'

    def test_set_constraints(self) -> None:
        """
        Function to test the methods to set constraints
        :return: None
        """
        stock_screener_constraints = StockScreenerConstraints
        magic_formula_constraints = stock_screener_constraints.set_constraints_magic_formula()
        assert type(magic_formula_constraints) == tuple
        assert len(magic_formula_constraints) == 2
        assert magic_formula_constraints[0]['screener'] == 'magic_formula'
