# I import the other modules
# I import argparse library (Python standard library) to create command-line application
# I import Counter (dict subclass) for counting hashable objects
import argparse
import corpus
import nb
from nb import SpamFilter
from collections import Counter
from pathlib import Path

# This function
def parse_args():
    parser = argparse.ArgumentParser(
        description="filters email contents dividing them into two categories: ham or spam"
    )  # the parser will hold all the information necessary to parse the command-line into python datatypes
    parser.add_argument(
        "-tr",
        "--train_dataset",
        metavar="dataset path",
        required="True",
        type=str,
        help="enter a path to a dataset of emails on which the filter will be trained",
    )  # we define which arguments the program will require: we tell how to take strings in CLI and turn them into objects
    parser.add_argument(
        "-te",
        "--test_dataset",
        metavar="dataset path",
        required="True",
        type=str,
        help="enter a path to a dataset of emails on which the filter will be tested",
    )
    parser.add_argument(
        "-f",
        "--resultfile",
        metavar="file",
        required="True",
        type=str,
        help="enter a path to a file where you want the results to be stored",
    )
    parser.add_argument(
        "-ud",
        "--diremails_classify",
        metavar="dataset path",
        required="True",
        type=str,
        help="enter a path to a folder containing emails that you want to classify",
    )
    args = parser.parse_args()
    return args


def main():
    argums = parse_args()
    print("I am reading the datasets")
    read_train = corpus.read_dataset(argums.train_dataset)
    read_test = corpus.read_dataset(argums.test_dataset)

    # I create an instance of the class SpamFilter and apply the train method
    spam_filter = SpamFilter()
    print("I will now train the Spam Filter")
    spam_filter.train(read_train)
    # I create a counter with keys for later Precision and Recall of the spamfilter
    precis_rec = Counter({"TP": 0, "FN": 0, "FP": 0, "TN": 0})

    # I iterate over the content of the mail in the test dataset and classify them
    print("I will now start validating")
    for mail, label in read_test:
        score, prediction = spam_filter.classify(mail)
        # I calculate how many true positive, false negative, false positive, true negative predictions
        # I increase the counter of the true predictions
        if label == prediction:
            if label == "spam":
                precis_rec["TN"] += 1
            elif label == "ham":
                precis_rec["TP"] += 1
        # I increase the counter of the false predictions
        else:
            if label == "spam":
                precis_rec["FN"] += 1
            elif label == "ham":
                precis_rec["FP"] += 1

    # I calculate precision and recall with formulas, not scikit learn
    # For precision the formula is TP/(TP+FP), for recall the formula is TP/(TP+FN)
    precision = precis_rec["TP"] / (precis_rec["TP"] + precis_rec["FP"])
    recall = precis_rec["TP"] / (precis_rec["TP"] + precis_rec["FN"])
    print(f"{precision=} {recall=}")

    dataset_location = Path(argums.diremails_classify)
    assert dataset_location.is_dir()
    # opening a file for writing the classification results
    with open(argums.resultfile, "w") as final_file:
        print(f"I am storing the classified emails in the {argums.resultfile}")
        # for the user emails I iterate over their content and read it with read_file method
        for mailtoclass in dataset_location.glob("*.txt"):
            read_mail = corpus.read_file(mailtoclass)
            scoremail, label = spam_filter.classify(read_mail)
            final_file.write(f"{mailtoclass.name} {scoremail} {label}\n")


if __name__ == "__main__":
    main()
