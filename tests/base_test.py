import pytest

from hojo.base import BaseModel
from hojo.orm.manager import Manager
from hojo.schema import BaseSchema


class TestBaseModel:
    class MockModel(BaseModel):
        pass

    class AnotherMockModel(BaseModel):
        pass

    def test_subclass_registration(self):
        assert TestBaseModel.MockModel in BaseModel._registry
        assert TestBaseModel.AnotherMockModel in BaseModel._registry

    def test_manager_initialization(self):
        assert isinstance(TestBaseModel.MockModel.objects, Manager)

    def test_inheritance_from_base_schema(self):
        assert issubclass(TestBaseModel.MockModel, BaseModel)
        assert issubclass(TestBaseModel.MockModel, BaseSchema)
