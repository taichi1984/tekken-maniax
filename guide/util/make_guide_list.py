from guide.models import Evaluation


def make_guide_list_with_evaluation(guide_list):
    latest_guide_eva_dict_list = []
    evaluations = Evaluation.objects.all()

    for guide in guide_list:
        num_of_good_evaluations = 0
        num_of_bad_evaluations = 0

        for evaluation in evaluations:
            if (guide.id == evaluation.guide_id) & (evaluation.evaluation == 1):

                num_of_good_evaluations += 1
            if (guide.id == evaluation.guide_id) & (evaluation.evaluation == 2):
                num_of_bad_evaluations += 1

        latest_guide_eva_dict_list.append(
            {
                'guide': guide,
                'num_of_good_evaluations': num_of_good_evaluations,
                'num_of_bad_evaluations': num_of_bad_evaluations
            }
        )

    return latest_guide_eva_dict_list;