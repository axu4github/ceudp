# -*- coding: utf-8 -*-

import json
from collections import OrderedDict
from openapi_codec import OpenAPICodec
from openapi_codec.encode import generate_swagger_object
from coreapi import Document, Link, Field
from coreapi.compat import force_bytes
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_swagger.renderers import (
    SwaggerUIRenderer,
    OpenAPIRenderer
)


schema = Document(
    title="统一数据平台接口页面",
    content={
        "用户认证": {
            "login": Link(
                url="/api/management/login/",
                action="POST",
                fields=[
                    Field(
                        name="username",
                        required=True,
                        location="form",
                        description="登陆用户名"
                    ),
                    Field(
                        name="password",
                        required=True,
                        location="form",
                        description="登陆密码"
                    )
                ],
                description="用户登陆（获取用户Token）",
            ),
        },
        "用户管理": {
            "post:management_api:user-list": {
                "contents": Link(
                    url="/api/management/users/",
                    action="POST",
                    fields=[
                        Field(
                            name="username",
                            required=True,
                            location="form",
                            description="用户名"
                        ),
                        Field(
                            name="groups",
                            required=True,
                            location="form",
                            type="array",
                            description="用户组"
                        ),
                    ],
                    description="用户创建",
                ),
            },
            "get:management_api:user-list": Link(
                url="/api/management/users/",
                action="GET",
                description="用户列表查看",
            ),
            "get:management_api:user-detail": Link(
                url="/api/management/users/{id}",
                action="GET",
                fields=[
                    Field(
                        name="id",
                        required=True,
                        location="path",
                        description="用户ID"
                    ),
                ],
                description="用户详情查看",
            ),
        }
    }
)


class SwaggerSchemaView(APIView):

    authentication_classes = ()
    permission_classes = ()

    renderer_classes = [
        OpenAPIRenderer,
        SwaggerUIRenderer
    ]

    def load_swagger_json(self, doc):
        """
        加载自定义swagger.json文档
        """
        data = generate_swagger_object(doc)
        with open(settings.API_SCHEMA_PATH) as s:
            doc_json = json.load(s, object_pairs_hook=OrderedDict)

        data['paths'].update(doc_json.pop('paths'))
        data.update(doc_json)
        return OpenAPICodec().decode(force_bytes(json.dumps(data)))

    def get(self, request):
        # generator = SchemaGenerator(title='后端API文档')
        # schema = generator.get_schema(request=request)
        # document = self.load_swagger_json(schema)
        return Response(schema)
