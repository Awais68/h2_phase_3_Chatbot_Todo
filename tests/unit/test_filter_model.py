"""
Unit tests for FilterState model.
"""

import pytest
from datetime import date, timedelta
from src.models.filter import FilterState
from src.models.enums import Status, Priority


class TestFilterStateCreation:
    """Test FilterState initialization."""

    def test_empty_filter_state(self):
        """Test that default FilterState has no active filters."""
        f = FilterState()
        assert not f.is_active()
        assert f.status is None
        assert f.priority is None
        assert f.date_range is None
        assert f.search_keyword is None
        assert f.tags is None

    def test_filter_state_with_status(self):
        """Test FilterState with status filter."""
        f = FilterState(status=Status.PENDING)
        assert f.is_active()
        assert f.status == Status.PENDING

    def test_filter_state_with_priority(self):
        """Test FilterState with priority filter."""
        f = FilterState(priority=Priority.HIGH)
        assert f.is_active()
        assert f.priority == Priority.HIGH

    def test_filter_state_with_date_range(self):
        """Test FilterState with date range filter."""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        f = FilterState(date_range=(today, tomorrow))
        assert f.is_active()
        assert f.date_range == (today, tomorrow)

    def test_filter_state_with_search(self):
        """Test FilterState with search keyword."""
        f = FilterState(search_keyword="meeting")
        assert f.is_active()
        assert f.search_keyword == "meeting"

    def test_filter_state_with_tags(self):
        """Test FilterState with tags."""
        f = FilterState(tags=["work", "urgent"])
        assert f.is_active()
        assert f.tags == ["work", "urgent"]


class TestFilterStateDescribe:
    """Test FilterState.describe() method."""

    def test_describe_empty(self):
        """Test describe returns 'No filters' when inactive."""
        f = FilterState()
        assert f.describe() == "No filters"

    def test_describe_status_filter(self):
        """Test describe with status filter."""
        f = FilterState(status=Status.COMPLETED)
        assert "Completed" in f.describe()

    def test_describe_priority_filter(self):
        """Test describe with priority filter."""
        f = FilterState(priority=Priority.HIGH)
        assert "High" in f.describe()

    def test_describe_search(self):
        """Test describe with search keyword."""
        f = FilterState(search_keyword="test")
        assert 'Search="test"' in f.describe()

    def test_describe_multiple_filters(self):
        """Test describe with multiple filters."""
        f = FilterState(
            status=Status.PENDING,
            priority=Priority.HIGH,
            search_keyword="important"
        )
        desc = f.describe()
        assert "Pending" in desc
        assert "High" in desc
        assert 'Search="important"' in desc


class TestFilterStateClear:
    """Test FilterState.clear() method."""

    def test_clear_resets_all_fields(self):
        """Test that clear() resets all filter fields."""
        f = FilterState(
            status=Status.PENDING,
            priority=Priority.HIGH,
            date_range=(date.today(), date.today() + timedelta(days=1)),
            search_keyword="test",
            tags=["tag1", "tag2"]
        )
        assert f.is_active()

        f.clear()

        assert f.status is None
        assert f.priority is None
        assert f.date_range is None
        assert f.search_keyword is None
        assert f.tags is None
        assert not f.is_active()


class TestFilterStateIsActive:
    """Test FilterState.is_active() method."""

    def test_empty_is_inactive(self):
        """Test that empty FilterState is inactive."""
        f = FilterState()
        assert not f.is_active()

    def test_empty_tags_list_is_inactive(self):
        """Test that FilterState with empty tags list is inactive."""
        f = FilterState(tags=[])
        assert not f.is_active()

    def test_none_tags_is_inactive(self):
        """Test that FilterState with None tags is inactive."""
        f = FilterState(tags=None)
        assert not f.is_active()
