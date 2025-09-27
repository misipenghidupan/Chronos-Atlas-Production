from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    # Django Admin Site
    path('admin/', admin.site.urls),

    # GraphQL Endpoint
    # We use csrf_exempt because the GraphQLView handles its own CSRF/security.
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]