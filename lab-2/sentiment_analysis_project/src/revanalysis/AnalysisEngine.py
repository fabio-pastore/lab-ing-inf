from model.BasicModel import BasicModel
from model.WordModel import WordModel

class AnalysisEngine():

    MIN_LINE_LENGTH: int = 3 # we need at least a character and an integer (0/1), separated by a comma
    INPUT_FILE: str = "IMDB_validation.csv"
    OUTPUT_FILE: str = "output_predictions.csv"

    def __init__(self):
        pass

    def start_analysis(self) -> None:
        """
        Manages the main flow for training and evaluating the models.
        
        It opens the input file to read the reviews and splits them in half: the first part is used to train the WordModel and the BasicModel. The second half is used
        as a test set to generate predictions, calculate the relative accuracy percentages, and print the results. Finally, it writes an output CSV file with the predicted labels.
        
        Args:
            None.
            
        Returns:
            None.
        """
        data_set_size: int = 0
        with open(AnalysisEngine.INPUT_FILE, "r", encoding="UTF-8") as fin:

            print("[AnalysisEngine] '" + AnalysisEngine.INPUT_FILE + "' opened successfully.")
            
            fin.readline() # ignore csv header
            file_data: list[str] = fin.readlines()
            data_set_size: int = len(file_data)
        
            training_data: list[tuple[str, int]] = []
            line_index: int = 0
            half_line_index: int = data_set_size // 2

            print("[AnalysisEngine] Beginning training for WordModel and BasicModel...")

            while (line_index < half_line_index):
                line_data: str = file_data[line_index].strip() 
                if len(line_data) >= AnalysisEngine.MIN_LINE_LENGTH:
                    review_data: list[str] = line_data.rsplit(",", 1)
                    review_text: str = review_data[0]
                    review_sentiment: int = int(review_data[1])
                    training_data.append((review_text, review_sentiment))
                line_index += 1

            wm: WordModel = WordModel() 
            bm: BasicModel = BasicModel()

            wm.analyze(training_data)
            bm.analyze(training_data)

            print("[AnalysisEngine] Training completed successfully!")

            total_reviews: int = 0
            wm_predictions: list[int] = []
            correct_wm: int = 0
            bm_predictions: list[int] = []
            correct_bm: int = 0

            with open(AnalysisEngine.OUTPUT_FILE, "w", encoding="UTF-8") as fout:
                print("[AnalysisEngine] '" + AnalysisEngine.OUTPUT_FILE + "' opened successfully.")
                print("[AnalysisEngine] Sentiment analysis in progress...")
                fout.write("text, label, predicted label\n") # write csv header
                while (line_index < data_set_size):
                    line_data: str = file_data[line_index].strip()
                    if len(line_data) >= AnalysisEngine.MIN_LINE_LENGTH:
                        total_reviews += 1
                        review_data: list[str] = line_data.rsplit(",", 1)
                        review_text: str = review_data[0]
                        actual_review_sentiment: int = int(review_data[1])
                        fout.write(line_data + ", ")

                        wm_prediction: int = wm.predict(review_text)
                        bm_predicition: int = bm.predict(review_text)

                        if (wm_prediction == actual_review_sentiment):
                            correct_wm += 1
                        if (bm_predicition == actual_review_sentiment):
                            correct_bm += 1

                        fout.write(str(wm_prediction) + "\n")
                        wm_predictions.append(wm_prediction)
                        bm_predictions.append(bm_predicition)

                    line_index += 1

            print("[AnalysisEngine] Sentiment analysis completed successfully!")
            print("[AnalysisEngine] '" + AnalysisEngine.OUTPUT_FILE + "' closed successfully.")

        print("[AnalysisEngine] '" + AnalysisEngine.INPUT_FILE + "' closed successfully.")
        print("[AnalysisEngine] WORD_MODEL_PERF: " + str(round(100 * (correct_wm/total_reviews), 4)) + "% of predictions were correct.")
        print("[AnalysisEngine] BASIC_MODEL_PERF: " + str(round(100 * (correct_bm/total_reviews), 4)) + "% of predictions were correct.")



        
        
            
