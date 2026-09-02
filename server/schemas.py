from marshmallow import fields

from server.extensions import ma
from server.models import (
    CollectionUnit,
    CuratorialUnitDefinition,
    Division,
    GeographicOrigin,
    GeologicalTimePeriod,
    LibraryAndArchivesFunction,
    StorageContainer,
    StorageRoom,
    Users,
)


class GeographicOriginDDSchema(ma.SQLAlchemyAutoSchema):
    """Creates a schema to be used in dropdown fields."""

    class Meta:
        model = GeographicOrigin
        exclude = ('geographic_origin_name', 'geographic_origin_id')

    label = fields.String(attribute='geographic_origin_name')
    value = fields.String(attribute='geographic_origin_id')


class GeologicalTimePeriodDDSchema(ma.SQLAlchemyAutoSchema):
    """Creates a schema to be used in dropdown fields."""

    class Meta:
        model = GeologicalTimePeriod
        exclude = ('period_name', 'geological_time_period_id')

    label = fields.String(attribute='period_name')
    value = fields.String(attribute='geological_time_period_id')


class DivisionDDSchema(ma.SQLAlchemyAutoSchema):
    """Creates a schema to be used in dropdown fields."""

    class Meta:
        model = Division

    label = fields.Method('get_label')
    value = fields.Method('get_value')
    division_id = fields.String()
    division_name = fields.String()

    def get_label(self, obj):
        return obj.division_name

    def get_value(self, obj):
        return obj.division_id


class StorageContainerDDSchema(ma.SQLAlchemyAutoSchema):
    """Creates a schema to be used in dropdown fields."""

    class Meta:
        model = StorageContainer
        exclude = ('container_name', 'storage_container_id')

    label = fields.String(attribute='container_name')
    value = fields.String(attribute='storage_container_id')


class StorageRoomDDSchema(ma.SQLAlchemyAutoSchema):
    """Creates a schema to be used in dropdown fields."""

    class Meta:
        model = StorageRoom
        exclude = ('room_code', 'storage_room_id')

    label = fields.String(attribute='room_code')
    value = fields.String(attribute='storage_room_id')


class TaxonDDSchema(ma.Schema):
    """Creates a schema to be used in dropdown fields."""

    label = fields.String()
    value = fields.String()


class CuratorialUnitDefinitionDDSchema(ma.SQLAlchemyAutoSchema):
    """Creates a schema to be used in dropdown fields."""

    class Meta:
        model = CuratorialUnitDefinition
        exclude = ('description', 'curatorial_unit_definition_id')

    label = fields.String(attribute='description')
    value = fields.String(attribute='curatorial_unit_definition_id')


class LibraryAndArchivesFunctionDDSchema(ma.SQLAlchemyAutoSchema):
    """Creates a schema to be used in dropdown fields."""

    class Meta:
        model = LibraryAndArchivesFunction
        exclude = ('function_name', 'library_and_archives_function_id')

    label = fields.String(attribute='function_name')
    value = fields.String(attribute='library_and_archives_function_id')


class UsersDDSchema(ma.SQLAlchemyAutoSchema):
    """Creates a schema to be used in dropdown fields."""

    class Meta:
        model = Users

    label = fields.Method('get_label')
    value = fields.Method('get_value')
    display_name = fields.String()
    user_id = fields.String()

    def get_label(self, obj):
        return obj.display_name

    def get_value(self, obj):
        return obj.user_id


class UnitByUsersSchema(ma.SQLAlchemyAutoSchema):
    """Creates a schema for the units by users endpoint."""

    class Meta:
        model = CollectionUnit

    last_rescored = fields.Date(load_default=None)
    last_assessed = fields.Date(load_default=None)
    division_name = fields.String(attribute='section.division.division_name')
    section_name = fields.String(attribute='section.section_name')
