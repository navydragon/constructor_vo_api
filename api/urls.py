from django.urls import include, path



from .views import EducationLevelListView, EducationDirectionListView,\
    ProgramViewSet, ProgramRoleListView, ProgramInformationView, \
    MyProgramsListView

from products.views import ProductViewSet, LifeStageViewSet, ProcessViewSet, ProcessListView
from competenceprofile.views import AbilityViewSet, CreateAbilityFromProcess, \
    AttachAbilityView, DetachAbilityView, KnowledgeViewSet, CreateKnowledgeFromAbility, \
    AttachKnowledgeView, DetachKnowledgeView

from disciplines.views import DisciplineViewSet, AttachKnowledgeToDisciplineView, \
DetachKnowledgeFromDisciplineView, AttachAbilityToDisciplineView, DetachAbilityFromDisciplineView

from assessment.views import QuestionViewSet, QuestionTypeListView

from users.views import UserListView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'programs', ProgramViewSet)
router.register(r'programs/(?P<program_id>\d+)/products', ProductViewSet)
router.register(r'products/(?P<product_id>\d+)/stages', LifeStageViewSet)
router.register(r'stages/(?P<stage_id>\d+)/processes', ProcessViewSet)
router.register(r'programs/(?P<program_id>\d+)/abilities', AbilityViewSet)
router.register(r'programs/(?P<program_id>\d+)/knowledges', KnowledgeViewSet)
router.register(r'programs/(?P<program_id>\d+)/disciplines', DisciplineViewSet)
router.register(r'knowledges/(?P<knowledge_id>\d+)/questions', QuestionViewSet)


urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),

    path('education_levels/', EducationLevelListView.as_view()),
    path('education_directions/', EducationDirectionListView.as_view()),
    path('program_roles/', ProgramRoleListView.as_view()),
    path('my_programs/', MyProgramsListView.as_view()),
    path('question_types/', QuestionTypeListView.as_view()),

    path('users/', UserListView.as_view()),

    path('programs/<int:pk>/information/', ProgramInformationView.as_view()),
    path('programs/<int:program_id>/processes/', ProcessListView.as_view()),
    path('processes/<int:process_id>/attach_ability/<int:ability_id>/', AttachAbilityView.as_view()),
    path('processes/<int:process_id>/detach_ability/<int:ability_id>/', DetachAbilityView.as_view()),
    path('processes/<int:process_id>/abilities/', CreateAbilityFromProcess.as_view()),

    path('abilities/<int:ability_id>/attach_knowledge/<int:knowledge_id>/', AttachKnowledgeView.as_view()),
    path('abilities/<int:ability_id>/detach_knowledge/<int:knowledge_id>/', DetachKnowledgeView.as_view()),
    path('abilities/<int:ability_id>/knowledges/', CreateKnowledgeFromAbility.as_view()),

    path('disciplines/<int:discipline_id>/attach_knowledge/<int:knowledge_id>/', AttachKnowledgeToDisciplineView.as_view()),
    path('disciplines/<int:discipline_id>/detach_knowledge/<int:knowledge_id>/', DetachKnowledgeFromDisciplineView.as_view()),
    path('disciplines/<int:discipline_id>/attach_ability/<int:ability_id>/', AttachAbilityToDisciplineView.as_view()),
    path('disciplines/<int:discipline_id>/detach_ability/<int:ability_id>/', DetachAbilityFromDisciplineView.as_view()),

] + router.urls