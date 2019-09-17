from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action


from problem.serializers import *
from .utils import CrawlerController, update_problem


controller = CrawlerController.get_controller()


class MemberViewSet(ModelViewSet):
    """
    doc TODO
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = []


class TeamViewSet(ModelViewSet):
    """
    doc TODO
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = []


class ContestViewSet(ModelViewSet):
    """
    出题API

    HTML form形式下有Score,Submit,Accept,Ac rate in percent四种筛选方式

    分别代表对难度区间、提交数量区间、通过数量区间、ac率区间（百分率转为整数）进行筛选，四种筛选方式（如果有）的结果取并集。

    Team 为队伍ID

    Problem cnt 代表需要的题目数量

    Ignore date 代表忽略这天之前系统中的统计

    HTML form下目前不是很方便提交，因为有些项目是可选的。

    这个接口只有`team`和`problem_cnt`两个字段是必选。

    可在Raw Data下填充如下数据进行测试：

    {
        "team": 1,
        "problem_cnt": 100
    }
    """
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    permission_classes = []


class ProblemViewSet(ModelViewSet):
    """
    doc TODO
    """
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = []


class UpdateProblemAPIView(mixins.CreateModelMixin,
                           GenericViewSet):
    serializer_class = UpdateProblemSerializer


@api_view(['GET'])
def api_update_problem(request, oj_name, pid):
    try:
        saved_instance, _ = update_problem(oj_name, pid)

        msg = 'create {}-{} success' if _ else 'update {}-{} success'
        return Response({"message": msg.format(oj_name, pid)})

    except NotImplementedError as e:
        return Response({"message": str(e)})




