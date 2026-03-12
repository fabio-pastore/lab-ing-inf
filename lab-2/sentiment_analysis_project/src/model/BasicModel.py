from model.Model import Model

class BasicModel(Model):
    def __init__(self):
        self.pos_counter: int = 0
        self.neg_counter: int = 0
        self.majority_class: int | None = None

    def analyze(self, review_data: list[tuple[str, int]]) -> None:
        """
        Calculates the majority class within the training dataset.
        
        It counts the total number of positive and negative reviews to determine which of the two classes is predominant, saving the result as
        the baseline model for future predictions.
        
        Args:
            review_data (list[tuple[str, int]]): A list containing the training data.
        
        Returns:
            None: This method modifies the object's internal state and does not return anything.
        """
        for review in review_data:
            opinion: int = review[1]
            if opinion:
                self.pos_counter += 1
            else:
                self.neg_counter += 1

        self.majority_class = 1 if self.pos_counter >= self.neg_counter else 0

    def predict(self, review: str) -> int:
        """
        Predicts the sentiment of a review relying solely on the majority class.
        
        This baseline model ignores the input review text and always returns the label of the most frequent class calculated during the training phase.
        
        Args:
            review (str): The review text (which is ignored by the internal logic).
        
        Returns:
            int: The value of the majority class (1 for positive, 0 for negative).
        """
        return self.majority_class
