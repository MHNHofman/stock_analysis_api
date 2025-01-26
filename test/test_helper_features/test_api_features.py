import pytest
import pandas as pd
from time import sleep
import time
from src.helper_features.api_features import SyncAPIFunctions, AsyncAPIFunctions

class TestSyncAPIFunctions:

    def test_calculate_duration(self):

        start_time = time.time()
        sleep_seconds = 2
        sleep(sleep_seconds)
        number_of_requests = 1
        duration = SyncAPIFunctions.calculate_duration(start_time, number_of_requests)
        # round the duration as an int in terms of seconds
        duration_in_seconds = round(duration)
        # ensure the sleep duration is equal to the calculated duration
        assert duration_in_seconds == sleep_seconds


class TestAsyncAPIFunctions:

    @pytest.mark.asyncio
    async def test_run_urls(self):

        response_data = {
            "status": "success",
            "json": {
                "id": 1,
                "name": "Sample Item",
                "description": "This is an example item in the API response.",
                "price": 19.99,
                "available": True
            },
            "message": "Data retrieved successfully."
        }


    @pytest.mark.asyncio
    async def test_handle_exceed_rates(self):

        rate = AsyncAPIFunctions.handle_api_exceed_rate(duration=60)
