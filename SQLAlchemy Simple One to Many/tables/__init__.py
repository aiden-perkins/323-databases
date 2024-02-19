from .Mixin import DepartmentMixin, CourseMixin, SectionMixin
from lib import IntrospectionFactory
# The following lines decide which class we want to be imported into main
# based on what we chose to do for the introspection question.
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES
introspection_type = IntrospectionFactory().introspection_type
if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:
    from .NoIntrospect import Department, Course, Section
elif introspection_type == INTROSPECT_TABLES:
    from .Introspect import Department, Course, Section
