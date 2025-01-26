# @pytest.mark.asyncio
# async def test_evaluate_trade_symbols(self) -> None:
#     """
#     Function to test whether stock can be found
#     :return: None
#     """
#     api_key = await AsyncAPIFunctions.async_load_api_keys()
#     trade_symbols = TradesOverview(api_key)
#     symbol_true = "MSFT"
#     symbol_false = "QiaoKeLi"
#     symbol_true_test = await trade_symbols.evaluate_trade_symbols(symbol=symbol_true)
#     assert symbol_true_test == symbol_true
#
#     with warnings.catch_warnings(record=True) as warn:
#         # Cause all warnings to always be triggered.
#         warnings.simplefilter("always")
#         # Trigger a warning
#         await trade_symbols.evaluate_trade_symbols(symbol=symbol_false)
#         # Verify the fake symbol triggers a warning
#         assert len(warn) == 1
#         assert issubclass(warn[-1].category, UserWarning)
#         assert "symbols" in str(warn[-1].message)