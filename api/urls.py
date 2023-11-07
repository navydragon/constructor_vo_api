from django.urls import include, path
from .views import EducationLevelListView, EducationDirectionListView,\
    ProgramViewSet, ProgramRoleListView, ProgramInformationView, \
    ProgramProductView, MyProgramsListView

from products.views import ProductViewSet, LifeStageViewSet, ProcessViewSet
from competenceprofile.views import AbilityView, AttachAbilityView, DetachAbilityView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'programs', ProgramViewSet)
router.register(r'programs/(?P<program_id>\d+)/products', ProductViewSet)
router.register(r'products/(?P<product_id>\d+)/stages', LifeStageViewSet)
router.register(r'stages/(?P<stage_id>\d+)/processes', ProcessViewSet)

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('education_levels/', EducationLevelListView.as_view()),
    path('education_directions/', EducationDirectionListView.as_view()),
    path('program_roles/', ProgramRoleListView.as_view()),
    path('my_programs/', MyProgramsListView.as_view()),
    path('programs/<int:pk>/information/', ProgramInformationView.as_view()),
    path('programs/<int:pk>/product/', ProgramProductView.as_view()),
    path('processes/<int:process_id>/abilities/', AbilityView.as_view()),
    path('processes/<int:process_id>/attach_ability/<int:ability_id>/', AttachAbilityView.as_view()),
    path('processes/<int:process_id>/detach_ability/<int:ability_id>/', DetachAbilityView.as_view()),
] + router.urls