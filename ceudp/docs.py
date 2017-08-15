# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework import viewsets
from django.shortcuts import render


class SwaggerSchemaView(viewsets.ViewSet):

    authentication_classes = ()
    permission_classes = ()

    def index(self, request):
        return render(request, "ceudp/docs.html", {
            "configuration": settings.DOCS_CONFIGURATION
        })
