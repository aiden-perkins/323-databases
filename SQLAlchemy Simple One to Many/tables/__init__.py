from .Mixin import DepartmentMixin, CourseMixin
from lib import IntrospectionFactory
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES
introspection_type = IntrospectionFactory().introspection_type
if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:
    from .NoIntrospect import DepartmentNoIntrospect as Department
    from .NoIntrospect import CourseNoIntrospect as Course
elif introspection_type == INTROSPECT_TABLES:
    from .Introspect import DepartmentIntrospect as Department
    from .Introspect import CourseIntrospect as Course
