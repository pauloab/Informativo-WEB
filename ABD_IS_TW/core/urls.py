from unicodedata import name
from django import views
from django.urls import path
from ABD_IS_TW.core import views

urlpatterns = [
    path("",views.index, name="index"),
    path("auth/login/",views.login,name="login"),
    path("auth/logout/",views.logout,name="logout"),
    path("user/info/",views.profile_info,name="userInfo"),
    path("user/edit/",views.profile_edit,name="editProfile"),
    path("articulo/<int:id>/",views.render_article,name="article"),
    path("category/<int:id>/",views.article_by_category,name="articleByCategory"),
    path("category/list/",views.categories, name="category_list"),
    path("category/delete/<int:id>/",views.delete_category, name="deleteCategory"),
    path("category/edit/<int:id>/",views.edit_category, name="editCategory"),
    path("category/add/",views.add_category, name="addCategory"),
    path("user/news/list/",views.user_news_list, name="userNewsList"),
    path("user/news/add/",views.add_user_new, name="addUserNew"),
    path("user/news/edit/<int:id>/", views.edit_user_new, name="editUserNew"),
    path("user/news/delete/<int:id>/", views.delete_user_new, name="deleteUserNew"),
    path("news/search/", views.search_article, name="searchArticle"),
    path("news/recents/", views.recientes, name="recents"),
    path("suscripcion/", views.suscribirse, name="suscribirse"),
    path("suscripcionList/delete/<int:id>/",views.delete_sub, name="deleteSub"),
    path("suscripcionList/", views.suscribirseList, name="suscribirseList"),
    path("sugerencias/", views.escribir_sugerencia, name="sugerencias"),
    path("sugerenciasList/", views.sugerencia_listar, name="sugerenciasList")
]
