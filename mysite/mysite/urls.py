from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from polls.models import Student, Teacher, Subject , Grade
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Serializers define the API representation.
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
# ViewSets define the view behavior.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# Serializers define the API representation.
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
# ViewSets define the view behavior.
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

# Serializers define the API representation.
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
# ViewSets define the view behavior.
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

# Serializers define the API representation.
class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    class Meta:
        model = Grade
        fields = '__all__'
# ViewSets define the view behavior.
class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'grades', GradeViewSet)

'''
Этот фрагмент кода связан с использованием библиотеки DRF-YASG
(Django REST framework Yet Another Swagger Generator), которая
позволяет автоматически генерировать документацию API на основе
спецификации OpenAPI/Swagger для Django REST Framework (DRF).
'''
schema_view = get_schema_view(
    openapi.Info(
        title="Your Project Title",
        default_version='v1',
        description="Тестовое описание",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snakesandrubies.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
