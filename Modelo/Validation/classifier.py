class DelayClassifier:

    @staticmethod
    def classify(value):

        if value <= 20:
            return "very_early"

        elif value <= 40:
            return "early"

        elif value <= 60:
            return "on_time"

        elif value <= 80:
            return "late"

        return "very_late"