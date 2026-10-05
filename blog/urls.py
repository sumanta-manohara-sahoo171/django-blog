from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_, name='logout'),
    path('profile/', profile, name='profile'),
    path('reset-password/', reset_password, name='reset_password'),
    path('update-profile/', update_profile, name='update_profile'),
    path('forgot-password/', forgot, name='forgot'),
    path('new-password/', new_password, name='new_password'),
    path('posts/', posts, name='posts'),
    path('post/<int:post_id>/', post_detail, name='post-detail'),
    path('new-blog/', create_post, name='create_post'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('update-post/<int:post_id>/', update_post, name='update_post'),
    path('my-posts/', my_posts, name='my_posts'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('post/<int:post_id>/react/<str:reaction_type>/', react_to_post, name='react_to_post'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
]