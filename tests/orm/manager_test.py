from unittest.mock import MagicMock, patch

import pytest

from hojo.base import BaseModel
from hojo.orm.manager import Manager
from hojo.schema import dataclass


@dataclass
class User(BaseModel):
    name: str


@pytest.fixture
def mock_get_queryset():
    with patch.object(Manager, "get_queryset") as mock:
        yield mock


@pytest.fixture
def mock_queryset(mock_get_queryset):
    mock_qs = MagicMock()
    mock_get_queryset.return_value = mock_qs
    return mock_qs


class TestManager:
    def test_all(self, mock_queryset):
        User.objects.all()
        mock_queryset.all.assert_called()

    def test_filter(self, mock_queryset):
        User.objects.filter(name="test")
        mock_queryset.filter.assert_called_with(name="test")

    def test_create(self, mock_queryset):
        test_data = {"field1": "value1", "field2": "value2"}
        User.objects.create(test_data)
        mock_queryset.create.assert_called_with(**test_data)

    def test_get(self, mock_queryset):
        User.objects.get(name="test")
        mock_queryset.get.assert_called_with(name="test")

    def test_get_or_create(self, mock_queryset):
        User.objects.get_or_create(name="test")
        mock_queryset.get_or_create.assert_called_with(name="test")

    def test_bulk_create(self, mock_queryset):
        objs = [User(name="test1"), User(name="test2")]
        User.objects.bulk_create(objs)
        mock_queryset.bulk_create.assert_called_with(objs)

    def test_bulk_update(self, mock_queryset):
        objs = [User(name="test1"), User(name="test2")]
        User.objects.bulk_update(objs)
        mock_queryset.bulk_update.assert_called_with(objs)

    def test_count(self, mock_queryset):
        User.objects.count()
        mock_queryset.count.assert_called()

    def test_order_by(self, mock_queryset):
        User.objects.order_by("name")
        mock_queryset.order_by.assert_called_with("name")

    def test_values(self, mock_queryset):
        User.objects.values("name")
        mock_queryset.values.assert_called_with("name")

    def test_values_list(self, mock_queryset):
        User.objects.values_list("name", flat=True)
        mock_queryset.values_list.assert_called_with("name", flat=True)

    def test_exists(self, mock_queryset):
        User.objects.exists()
        mock_queryset.exists.assert_called()

    def test_delete(self, mock_queryset):
        User.objects.delete()
        mock_queryset.delete.assert_called()

    def test_update(self, mock_queryset):
        update_data = {"name": "updated_name"}
        User.objects.update(**update_data)
        mock_queryset.update.assert_called_with(**update_data)

    def test_annotate(self, mock_queryset):
        User.objects.annotate(annotation_field="value")
        mock_queryset.annotate.assert_called_with(annotation_field="value")

    def test_aggregate(self, mock_queryset):
        User.objects.aggregate(field="value")
        mock_queryset.aggregate.assert_called_with(field="value")

    def test_reverse(self, mock_queryset):
        User.objects.reverse()
        mock_queryset.reverse.assert_called()

    def test_distinct(self, mock_queryset):
        User.objects.distinct()
        mock_queryset.distinct.assert_called()

    def test_first(self, mock_queryset):
        User.objects.first()
        mock_queryset.first.assert_called()

    def test_last(self, mock_queryset):
        User.objects.last()
        mock_queryset.last.assert_called()
