from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from problem.serializers import *
from ojcrawler.control import Controller

controller = Controller()


class ProblemModelViewSet(ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = []


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

        instance.origin_link = url
        instance.content = data

        instance.save()
        msg = 'create {}-{} success' if _ else 'update {}-{} success'
        return Response({"message": msg.format(oj_name, pid)})

    except NotImplementedError as e:
        return Response({"message": str(e)})
