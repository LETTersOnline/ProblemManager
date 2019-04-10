"""ProblemManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from collections import OrderedDict

from django.contrib import admin
from django.urls import path, include
from problem.views import *
from django.urls import NoReverseMatch
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter, APIRootView


class CustomAPIRootView(APIRootView):
    """
    API ROOT, doc TBC
    """
    def get(self, request, *args, **kwargs):
        # Return a plain {"name": "hyperlink"} response.
        ret = OrderedDict()
        namespace = request.resolver_match.namespace
        for key, url_name in self.api_root_dict.items():
            if namespace:
                url_name = namespace + ':' + url_name
            try:
                ret[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get('format', None)
                )
            except NoReverseMatch:
                # Don't bail out if eg. no list routes exist, only detail routes.
                continue
        ret['update POJ problem'] = reverse(
            'update-problem',
            args=('poj', '1000'),
            kwargs=kwargs,
            request=request,
            format=kwargs.get('format', None)
        )
        ret['update HDU problem'] = reverse(
            'update-problem',
            args=('HDU', '1000'),
            kwargs=kwargs,
            request=request,
            format=kwargs.get('format', None)
        )
        ret['update CF problem'] = reverse(
            'update-problem',
            args=('codeforces', '100A'),
            kwargs=kwargs,
            request=request,
            format=kwargs.get('format', None)
        )
        return Response(ret)


class CustomRouter(DefaultRouter):
    APIRootView = CustomAPIRootView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),

    path('problems/update/<oj_name>/<pid>/', update_problem, name='update-problem'),
]

router = CustomRouter()

router.register(r'problems', ProblemViewSet, basename='problems')
router.register(r'contests', ContestViewSet, basename='contests')
router.register(r'teams', TeamViewSet, basename='teams')
router.register(r'members', MemberViewSet, basename='members')
urlpatterns += router.urls
