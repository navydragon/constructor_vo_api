from django.urls import include, path
from .views import EducationLevelListView, EducationDirectionListView,\
    ProgramViewSet, ProgramRoleListView, ProgramInformationView, MyProgramsListView

from products.views import ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'programs', ProgramViewSet)
router.register(r'programs/(?P<program_id>\d+)/products', ProductViewSet)

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('education_levels/', EducationLevelListView.as_view()),
    path('education_directions/', EducationDirectionListView.as_view()),
    path('program_roles/', ProgramRoleListView.as_view()),
    path('my_programs/', MyProgramsListView.as_view()),
    path('programs/<int:pk>/information', ProgramInformationView.as_view()),
] + router.urls