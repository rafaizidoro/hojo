from dataclasses import dataclass, field
from typing import Optional
from unittest.mock import Mock, patch

import pytest

from hojo.orm.queryset import LookupFilter, QuerySet


class MockAlchemy:
    def __init__(self, *args, **kwargs):
        self._result = []

    def where(self, *args, **kwargs):
        return self

    def values(self, *args, **kwargs):
        return self

    def all(self):
        return self._result

    def first(self):
        return self._result[0] if self._result else None

    def scalars(self):
        return self

    def set_result(self, result):
        self._result = result


def mock_select(*args, **kwargs):
    return MockAlchemy(*args, **kwargs)


def mock_update(*args, **kwargs):
    return MockAlchemy(*args, **kwargs)


def mock_delete(*args, **kwargs):
    return MockAlchemy(*args, **kwargs)


def mock_session():
    return Mock(execute=Mock(return_value=MockAlchemy()))


class MockModel:
    def __init__(self, name=None, age=None, occupation=None):
        self._name = name
        self._age = age
        self._occupation = occupation
        self.field = None

    @property
    def name(self):
        self.field = "name"
        return self

    @property
    def age(self):
        self.field = "age"
        return self

    @property
    def occupation(self):
        self.field = "occupation"
        return self

    def __eq__(self, other):
        return f"{self.field} == '{other}'"

    def __gt__(self, other):
        return f"{self.field} > {other}"

    def __ge__(self, other):
        return f"{self.field} >= {other}"

    def __lt__(self, other):
        return f"{self.field} < {other}"

    def __le__(self, other):
        return f"{self.field} <= {other}"

    def in_(self, values):
        return f"{self.field} in {values}"

    def is_(self, value):
        return f"{self.field} is {'None' if value is None else value}"

    def between(self, start, end):
        return f"{self.field} between {start} and {end}"


@pytest.fixture
def session():
    return mock_session()


@pytest.fixture
def queryset(session: Mock):
    return QuerySet(MockModel(), session)  # type: ignore


@pytest.fixture(autouse=True)
def apply_patches():
    with patch(
        "hojo.orm.queryset.select", side_effect=mock_select
    ) as mock_select_patch, patch(
        "hojo.orm.queryset.update", side_effect=mock_update
    ) as mock_update_patch, patch(
        "hojo.orm.queryset.delete", side_effect=mock_delete
    ) as mock_delete_patch:
        yield


class TestQuerySetFilters:
    def test_eq_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(name="Sephiroth")
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [
            LookupFilter("name", "eq", "Sephiroth", False)
        ]

    def test_gt_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(age__gt=30)
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [LookupFilter("age", "gt", 30, False)]

    def test_gte_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(age__gte=30)
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [LookupFilter("age", "gte", 30, False)]

    def test_multiple_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(name="Sephiroth").filter(age__gt=10)
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [
            LookupFilter("name", "eq", "Sephiroth", False),
            LookupFilter("age", "gt", 10, False),
        ]

    def test_lt_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(age__lt=30)
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [LookupFilter("age", "lt", 30, False)]

    def test_lte_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(age__lte=30)
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [LookupFilter("age", "lte", 30, False)]

    def test_isnull_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(occupation__isnull=True)
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [
            LookupFilter("occupation", "isnull", True, False)
        ]

    def test_in_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(age__in=[25, 30, 35])
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [
            LookupFilter("age", "in", [25, 30, 35], False)
        ]

    def test_between_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(age__between=(25, 35))
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [
            LookupFilter("age", "between", (25, 35), False)
        ]

    def test_like_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(name__like="Sephiroth")
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [
            LookupFilter("name", "like", "Sephiroth", False)
        ]

    def test_ilike_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(name__ilike="Sephiroth")
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [
            LookupFilter("name", "ilike", "Sephiroth", False)
        ]

    def test_contains_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(name__contains="roth")
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [
            LookupFilter("name", "contains", "roth", False)
        ]

    def test_startswith_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(name__startswith="S")
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [
            LookupFilter("name", "startswith", "S", False)
        ]

    def test_endswith_filter(self, queryset: QuerySet):
        filtered_qs = queryset.filter(name__endswith="oth")
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [
            LookupFilter("name", "endswith", "oth", False)
        ]


class TestQuerySetConditions:
    def test_eq_compile_condition(self, queryset: QuerySet):
        qs = queryset.filter(name="Sephiroth")
        conditions = qs.compile_conditions()
        assert len(conditions) == 1
        assert str(conditions[0]) == "name == 'Sephiroth'"

    def test_gt_compile_condition(self, queryset: QuerySet):
        qs = queryset.filter(age__gt=30)
        conditions = qs.compile_conditions()
        assert len(conditions) == 1
        assert str(conditions[0]) == "age > 30"

    def test_ge_compile_condition(self, queryset: QuerySet):
        qs = queryset.filter(age__gte=30)
        conditions = qs.compile_conditions()
        assert len(conditions) == 1
        assert str(conditions[0]) == "age >= 30"

    def test_lt_compile_condition(self, queryset: QuerySet):
        qs = queryset.filter(age__lt=30)
        conditions = qs.compile_conditions()
        assert len(conditions) == 1
        assert str(conditions[0]) == "age < 30"

    def test_le_compile_condition(self, queryset: QuerySet):
        qs = queryset.filter(age__lte=30)
        conditions = qs.compile_conditions()
        assert len(conditions) == 1
        assert str(conditions[0]) == "age <= 30"

    def test_in_compile_condition(self, queryset: QuerySet):
        qs = queryset.filter(age__in=[25, 30, 35])
        conditions = qs.compile_conditions()
        assert len(conditions) == 1
        assert str(conditions[0]) == "age in [25, 30, 35]"

    def test_isnull_compile_condition(self, queryset: QuerySet):
        qs = queryset.filter(occupation__isnull=True)
        conditions = qs.compile_conditions()
        assert len(conditions) == 1
        assert str(conditions[0]) == "occupation is None"

    def test_between_compile_condition(self, queryset: QuerySet):
        qs = queryset.filter(age__between=(25, 35))
        conditions = qs.compile_conditions()
        assert len(conditions) == 1
        assert str(conditions[0]) == "age between 25 and 35"


class TestQuerySet:
    def test_exclude(self, queryset: QuerySet):
        filtered_qs = queryset.filter(name="Sephiroth").exclude(age__gt=10)
        assert isinstance(filtered_qs, QuerySet)
        assert filtered_qs.lookup_filters == [
            LookupFilter("name", "eq", "Sephiroth", False),
            LookupFilter("age", "gt", 10, True),
        ]

    def test_all(self, queryset: QuerySet):
        query1 = queryset.all()
        query2 = queryset.all()

        assert str(query1) == "<QuerySet [not executed]>"
        assert str(query2) == "<QuerySet [not executed]>"

        assert query1 != query2

    def test_query_execution(self, queryset: QuerySet):
        mock_result = [MockModel(name="Cloud", age=35), MockModel(name="Tifa", age=28)]
        queryset.session.execute.return_value.set_result(mock_result)

        result = list(queryset.filter(name="Tifa").all())

        assert len(result) == 2
        assert all(isinstance(item, MockModel) for item in result)
