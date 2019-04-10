from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from problem.serializers import *
from ojcrawler.control import Controller
from rest_framework.decorators import action


controller = Controller()


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = []


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = []


class ContestViewSet(ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    permission_classes = []


class ProblemViewSet(ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = []


class UpdateProblemAPIView(mixins.CreateModelMixin,
                           GenericViewSet):
    serializer_class = UpdateProblemSerializer


@api_view(['GET'])
def update_problem(request, oj_name, pid):
    try:
        _, data = controller.get_problem(oj_name, pid)
        if not _:
            return Response({"message": "update problem failed."})
        url = controller.static_supports[oj_name].url_problem(pid)
        instance, _ = Problem.objects.get_or_create(oj=oj_name, pid=pid)

        if data.get('accepted_number', None) is not None:
            instance.accepted_number = data.get('accepted_number')

        if data.get('submitted_number', None) is not None:
            instance.submitted_number = data.get('submitted_number')

        if data.get('difficult_number', None) is not None:
            instance.difficult_number = data.get('difficult_number')

        if instance.accepted_number != -1 and instance.submitted_number != -1:
            instance.ac_rate_in_percent = int(100.0 * instance.accepted_number / instance.submitted_number)

        instance.origin_link = url
        instance.content = data

        instance.save()
        msg = 'create {}-{} success' if _ else 'update {}-{} success'
        return Response({"message": msg.format(oj_name, pid)})

    except NotImplementedError as e:
        return Response({"message": str(e)})




