from django.conf.urls import url
from myapp import views

urlpatterns = [
        url(r'^$',views.PostListView.as_view(),name='post_list'),
        url(r'^post/myposts/',views.MyPostListView.as_view(),name='my_list'),
        url(r'^post/(?P<pk>\d+)$',views.PostDetailView.as_view(),name='post_detail'),
        url(r'^post/new/$',views.CreatepostView.as_view(),name='post_new'),
        url(r'^post/(?P<pk>\d+)/edit/$',views.UpdatePostview.as_view(),name='post_edit'),
        url(r'^post/(?P<pk>\d+)/remove/$',views.PostDeleteView.as_view(),name='post_remove'),
        url(r'^drafts/$',views.DraftListView.as_view(),name='post_draft_list'),
        url(r'^post/(?P<pk>\d+)/comment/$',views.add_comment,name='add_comment'),
        url(r'^comment/(?P<pk>\d+)/approve/$',views.approve_comment,name='approve_comment'),
        url(r'^comment/(?P<pk>\d+)/remove/$',views.remove_comment,name='remove_comment'),
        url(r'^post/(?P<pk>\d+)/publish/$',views.publish_post,name='publish_post'),
]
