from django.urls import path
from .views import (
    home,
    post,
    nosotros,
    contactos,
    upload_post,
    add_comment,
    register,
    user_login,
    user_logout,
    crear_avatar,
    editar_perfil,
    mi_cuenta,
    perfil,
    admin_dashboard,
    admin_delete_post,
    admin_delete_comment,
    admin_delete_user,
)



urlpatterns = [
    path('', home, name='home'),
    path('post/', post, name='post'),
    path('nosotros/', nosotros, name='nosotros'),
    path('contactos/', contactos, name='contactos'),
    path('upload/',upload_post, name='upload_post'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path("crear-avatar/", crear_avatar, name="crear-avatar"),
    path("editar_perfil/", editar_perfil, name="editar_perfil"),
    path("perfil/", perfil, name="perfil"),
    path("mi_cuenta/", mi_cuenta, name="mi_cuenta"),
    ################ADMIN#######################
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/delete_post/<int:post_id>/', admin_delete_post, name='admin_delete_post'),
    path('admin/delete_comment/<int:comment_id>/', admin_delete_comment, name='admin_delete_comment'),
    path('admin/delete_user/<int:user_id>/', admin_delete_user, name='admin_delete_user'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)