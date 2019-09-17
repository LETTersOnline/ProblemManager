from ojcrawler.control import Controller

from .models import Problem

class CrawlerController:
    controller = Controller()

    @staticmethod
    def get_controller():
        return CrawlerController.controller


def update_problem(oj_name, pid):
    controller = CrawlerController.get_controller()

    _, data = controller.get_problem(oj_name, pid)
    if not _:
        raise ValueError("update problem failed.")
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
    return instance, _
