from django.urls import path,include
from . import views
#============================================student urls=============================================================#
urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.home,name='home'),
    path('ccoding',views.ccoding,name='ccoding'),
    path('pcoding',views.pcoding,name='pcoding'),
    path('pyevaluate',views.pyevaluate,name="pyevaluate"),
    path('pyquestions/<int:id>',views.pyquestions,name="pyquestions"),
    path('register',views.register,name="register"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('slist',views.slist,name='slist'),
    path('startquiz/<int:id>',views.startquiz,name='startquiz'),
    path('evaluate',views.evaluate,name='evaluate'),
    path('sresult',views.sresult,name='sresult'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('pleader',views.pleader,name='pleader'),
    path('csubmit',views.csubmit,name='csubmit'),
    path('pcode/<int:id>',views.pcode,name='pcode'),
    path('cquestions/<int:id>',views.cquestions,name="cquestions"),
    path('cevaluate',views.cevaluate,name="cevaluate"),
    path('sdashboard',views.sdashboard,name='sdashboard'),
#=====================================================================================================================#
#================================staff urls====================================================#
    path('createquiz',views.createquiz,name="createquiz"),
    path('validquiz',views.validquiz,name='validquiz'),
    path('listquiz',views.listquiz,name='listquiz'),
    path('open/<int:id>',views.open,name='open'),
    path('question/<int:id>',views.question,name='question'),
    path('addquestion',views.addquestion,name='addquestion'),
    path('deletequiz/<int:id>',views.deletequiz,name='deletequiz'),
    path('deletequestion/<int:id>/<int:qid>',views.deletequestion,name='deletequestion'),
    path('editquestion/<int:id>/<int:qid>',views.editquestion,name='editquestion'),
    path('updatequiz',views.updatequiz,name='updatequiz'),
    path('result/<int:id>',views.result,name='result'),
]
