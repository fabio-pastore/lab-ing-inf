from model.Model import Model
import string

class WordModel(Model):

    # The following values were found through trial and error and seem to be optimal for this dataset. (77.5% correct prediction rate for the WordModel!)
    MAX_THRESHOLD: int = 100 # IDEA: ignore excessively common words
    MIN_THRESHOLD: int = 3  # IDEA: ignore excessively rare words

    def __init__(self):
        self.pos_words: dict[str, int] = {}
        self.neg_words: dict[str, int] = {}
        self.assessed_positive: set[str] = set()
        self.assessed_negative: set[str] = set()
        self.punctuation_remover: dict[int, int | None] = str.maketrans('', '', string.punctuation)

    def analyze(self, review_data: list[tuple[str, int]]) -> None:
        """
        Analyzes a training dataset to identify positive and negative words.
        
        It cleans the reviews by removing punctuation, counts the occurrences of each word in positive and negative texts, and selects the "key" words. Words are
        classified as positive or negative based on whether they fall within a minimum and maximum frequency threshold, populating the model's internal sets.
        
        Args:
            review_data (list[tuple[str, int]]): A list containing the training data. Each element is a tuple with the review text and its label (1=positive, 0=negative).
        
        Returns:
            None: This method modifies the object's internal state and does not return anything.
        """
        for rev in review_data:
            rev_content: str = rev[0]
            is_pos_review: bool = rev[1]
            clean_rev: str = rev_content.translate(self.punctuation_remover).strip().lower()
            words_rev: list[str] = clean_rev.split()
            for w in words_rev:
                if w not in self.pos_words:
                    self.pos_words[w] = 0
                if w not in self.neg_words:
                    self.neg_words[w] = 0

                if is_pos_review:
                    self.pos_words[w] += 1
                else:
                    self.neg_words[w] += 1

        for w in self.pos_words:
            if (self.pos_words[w] > self.neg_words[w] and abs(self.pos_words[w] - self.neg_words[w]) > WordModel.MIN_THRESHOLD and self.pos_words[w] < WordModel.MAX_THRESHOLD and self.neg_words[w] < WordModel.MAX_THRESHOLD):
                self.assessed_positive.add(w)
            elif (self.neg_words[w] > self.pos_words[w] and abs(self.neg_words[w] - self.pos_words[w]) > WordModel.MIN_THRESHOLD and self.pos_words[w] < WordModel.MAX_THRESHOLD and self.neg_words[w] < WordModel.MAX_THRESHOLD):
                self.assessed_negative.add(w)
            else:
                pass

    def predict(self, review: str) -> int:
        """
        Predicts the sentiment of a single review based on the learned dictionary.
        
        It removes punctuation from the input string and compares the found words with the sets of positive and negative words generated during the training phase.
        The predicted class is the one that gets the highest number of matches.
        
        Args:
            review (str): The string containing the review text to be evaluated.
        
        Returns:
            int: 1 if the model predicts a positive review, 0 if negative.
        """
        pos_w_counter: int = 0
        neg_w_counter: int = 0
        clean_rev: str = review.translate(self.punctuation_remover).strip().lower()
        words_rev: list[str] = clean_rev.split() 
        for w in words_rev:
            if w in self.assessed_positive:
                pos_w_counter += 1
            elif w in self.assessed_negative:
                neg_w_counter += 1
            else:
                pass
        if pos_w_counter >= neg_w_counter:
            return 1 # predict positive review
        else:
            return 0 # predict negative review

        



        
                