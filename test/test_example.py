# import unittest
# from unittest.mock import AsyncMock
# import pytest
# from abc import ABC, abstractmethod
# from datetime import datetime as dt
#
#
# class BasePatient(ABC):
#     def __init__(self, data: dict) -> None:
#         self.first_name = data.get("first_name", "N/A")
#         self.last_name = data.get("last_name", "N/A")
#
#     @property
#     @abstractmethod
#     def initials(self) -> str:
#         """Return patient inititals"""
#
#     def to_fhir(self) -> dict:
#         return {
#             "Patient":{
#                 "first_name": self.first_name,
#                 "last_name": self.last_name
#             },
#             "metadata": {
#                 "created_at": dt.now()
#             }
#         }
#
#     @property
#     def full_name(self) -> str:
#         return f"{self.first_name} {self.last_name}"
#
#     @property
#     def account(self) -> str:
#         raise NotImplementedError()
#
# # bp = BasePatient({"first_name": "John", "last_name": "Doe"}) # error
#
#
# class Patient(BasePatient):
#     def initials(self) -> str:
#         return f"{self.first_name[0]}. {self.last_name[0]}."
#
#
# class FinancialPatient(BasePatient):
#     def __init__(self, data: dict) -> None:
#         super().__init__(data)
#         self._account = data.get("account", "")
#
#     @property
#     def initials(self) -> str:
#         return f"{self.first_name[0]}. {self.last_name}"
#
#     @property
#     def account(self) -> str:
#         return f"NL {self._account}"
#
#
#
#
#
#
#
# @pytest.fixture
# def mock_thing() -> AsyncMock:
#     """
#     Async Mock Fixture
#     :return:
#     """
#     mock_thing = AsyncMock()
#     mock_thing.CatFact.get_cat_fact = AsyncMock(
#         return_value="Mother cats " "teach their kittens " "to use the litter box."
#     )
#     return mock_thing
#
#
# @pytest.mark.asyncio
# async def test_get_cat_fact_mock(mock_thing) -> None:
#     """
#     Test for get_cat_fact method using Async Mocking
#     :param mock_thing: Mock fixture
#     :return: None
#     """
#     result = await mock_thing.CatFact.get_cat_fact()
#     assert result == "Mother cats teach their kittens to use the litter box."
#
#
#
# class TestAbstract:
#     def test_abstract(self):
#         print('ok')
#
#         patient_data = {
#             "first_name": "John",
#             "last_name": "Doe",
#             "account": "1234567890",
#         }
#         p = Patient(patient_data)
#         print(p.full_name)
#         print(p.to_fhir())
#
#         fa_patient = FinancialPatient(patient_data)
#         print(fa_patient.initials)
#         print(fa_patient.account)
#         print(fa_patient.to_fhir())


# from fastapi import FastAPI
# import pytest
#
#
# app = FastAPI()


# @pytest.mark.asyncio
# async def test_fast_api():
#     """
#     Function to test whether stock can be found
#     :return: None
#     """
#
#     new_test = await root()
#     print('ok')
#
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

from src.random_scripts import get_excel

def test_get_excel():
    get_excel()
    print('ok')
    assert True

