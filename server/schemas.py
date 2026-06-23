from server.extensions import ma
from server.models import *


class GeographicOriginDDSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GeographicOrigin
        exclude = ('geographic_origin_name', 'geographic_origin_id')

    label = ma.String(attribute='geographic_origin_name')
    value = ma.String(attribute='geographic_origin_id')


class GeologicalTimePeriodDDSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GeologicalTimePeriod
        exclude = ('period_name', 'geological_time_period_id')

    label = ma.String(attribute='period_name')
    value = ma.String(attribute='geological_time_period_id')


class DivisionDDSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Division

    label = ma.Method('get_label')
    value = ma.Method('get_value')
    division_id = ma.String()
    division_name = ma.String()

    def get_label(self, obj):
        return obj.division_name

    def get_value(self, obj):
        return obj.division_id


class StorageContainerDDSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StorageContainer
        exclude = ('container_name', 'storage_container_id')

    label = ma.String(attribute='container_name')
    value = ma.String(attribute='storage_container_id')


class StorageRoomDDSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StorageRoom
        exclude = ('room_code', 'storage_room_id')

    label = ma.String(attribute='room_code')
    value = ma.String(attribute='storage_room_id')


class TaxonDDSchema(ma.Schema):
    label = ma.String()
    value = ma.String()


class CuratorialUnitDefinitionDDSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CuratorialUnitDefinition
        exclude = ('description', 'curatorial_unit_definition_id')

    label = ma.String(attribute='description')
    value = ma.String(attribute='curatorial_unit_definition_id')


class LibraryAndArchivesFunctionDDSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LibraryAndArchivesFunction
        exclude = ('function_name', 'library_and_archives_function_id')

    label = ma.String(attribute='function_name')
    value = ma.String(attribute='library_and_archives_function_id')


class UsersDDSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users

    label = ma.Method('get_label')
    value = ma.Method('get_value')
    display_name = ma.String()
    user_id = ma.String()

    def get_label(self, obj):
        return obj.display_name

    def get_value(self, obj):
        return obj.user_id


class UnitByUsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CollectionUnit

    last_rescored = ma.Date(load_default=None)
    last_assessed = ma.Date(load_default=None)
    section_name = ma.Method('get_section_name')
    division_name = ma.Method('get_division_name')

    def get_section_name(self, obj):
        return obj.section.section_name

    def get_division_name(self, obj):
        return obj.section.division.division_name


class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        include_only = ('display_name', 'email', 'role_id', 'division_id')

    role = ma.Method('get_role')
    level = ma.Method('get_level')
    role_id = ma.Method('get_role_id')

    def get_role(self, obj):
        return obj.roles.role

    def get_level(self, obj):
        return obj.roles.level

    def get_role_id(self, obj):
        return obj.roles.role_id
