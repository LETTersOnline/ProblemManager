import os
import django
import pprint
from bs4 import BeautifulSoup


def calc_title_equality(first_problem, second_problem):
    """
    return True if title is same otherwise False
    :param first_problem:
    :param second_problem:
    :return:
    """
    return first_problem.content['title'] == second_problem.content['title']


def longest_common_sequence(first_sequence, second_sequence):
    second_size = len(second_sequence)
    previous_state = [0 for _ in range(second_size + 1)]
    for i, fc in enumerate(first_sequence):
        second_state = [0]
        for j, sc in enumerate(second_sequence):
            second_state.append(previous_state[j + 1])
            if second_state[j] > second_state[j+1]:
                second_state[j+1] = second_state[j]
            if first_sequence[i] == second_sequence[j] and previous_state[j] + 1 > second_state[j+1]:
                second_state[j + 1] = previous_state[j] + 1
        previous_state, second_state = second_state, previous_state
    return previous_state[second_size]


def get_nested_text(d):
    if isinstance(d, str):
        return BeautifulSoup(d, features='html5lib').get_text()
    return '\n'.join(get_nested_text(x) for x in d)


def calc_description_similarity(first_words, second_words):
    lcs = longest_common_sequence(first_words, second_words)
    return (lcs ** 2) / len(first_words) / len(second_words)


def calc_cleaned_description_equality(first_words, second_words):
    return first_words == second_words


def main():
    from problem.models import Problem, ProblemSimilarity

    def similarity_task(first, second):
        ins = None
        inner_first, inner_first_cleaned_text = first
        inner_second, inner_second_cleaned_text = second
        if calc_cleaned_description_equality(inner_first_cleaned_text, inner_second_cleaned_text):
            if ins is None:
                ins, _ = ProblemSimilarity.objects.get_or_create(first=inner_first, second=inner_second)
            ins.description.update({'description_equality': 1})
        if ins:
            ins.save()

    all_problems = list((ins, get_nested_text(ins.content['descriptions']).split()) for ins in Problem.objects.all())

    cnt = 1

    for first_problem in all_problems:
        for second_problem in all_problems:
            if first_problem[0].id < second_problem[0].id:
                similarity_task(first_problem, second_problem)

            pprint.pprint((cnt, len(all_problems) ** 2))
            cnt += 1


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProblemManager.local_settings')
    django.setup()
    main()
