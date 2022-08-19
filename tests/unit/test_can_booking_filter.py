import pytest

from server import can_booking_filter
from tests.conftest import (generate_future_competitions,
                            generate_past_competitions)


class TestCanBookingFilter:

    @pytest.mark.parametrize("competition", generate_future_competitions())
    def test_competition_is_in_future(self, competition):
        competition_is_in_future = can_booking_filter(competition)
        assert competition_is_in_future

    @pytest.mark.parametrize("competition", generate_past_competitions())
    def test_competition_is_in_past(self, competition):
        competition_is_in_future = can_booking_filter(competition)
        assert not competition_is_in_future
