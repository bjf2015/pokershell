import collections

import minsk.eval.context as context

import minsk.eval.evaluators as evaluators
import minsk.model as model


class EvaluatorManager:
    _EVALUATORS = collections.OrderedDict([
        (model.Hand.STRAIGHT_FLUSH, evaluators.StraightFlushEvaluator()),
        (model.Hand.FOUR_OF_KIND, evaluators.FourEvaluator()),
        (model.Hand.FULL_HOUSE, evaluators.FullHouseEvaluator()),
        (model.Hand.FLUSH, evaluators.FlushEvaluator()),
        (model.Hand.STRAIGHT, evaluators.StraightEvaluator()),
        (model.Hand.THREE_OF_KIND, evaluators.ThreeEvaluator()),
        (model.Hand.TWO_PAIR, evaluators.TwoPairsEvaluator()),
        (model.Hand.ONE_PAIR, evaluators.OnePairEvaluator()),
        (model.Hand.HIGH_CARD, evaluators.HighCardEvaluator()),
    ])

    def find_best_hand(self, *args):
        ctx = context.EvalContext(*args)
        for hand, evaluator in self._EVALUATORS.items():
            result = evaluator.find(ctx)
            if result:
                return hand, result
