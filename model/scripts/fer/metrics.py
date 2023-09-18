import numpy as np

def main():
    """
    Script that calculates Metrics for our model, based on cofusion matrix
    :return:
    """
    matrix = np.array([[65, 20, 203, 86, 73],
                       [18, 4, 46, 26, 26],
                       [169, 40, 461, 261, 200],
                       [89, 26, 269, 142, 112],
                       [65, 14, 171, 107, 88]])

    # Calculate TP, FP, FN for each class
    TP = np.diag(matrix)
    FP = np.sum(matrix, axis=0) - TP
    FN = np.sum(matrix, axis=1) - TP

    # oblicz precision, recall i f1_score dla każdej klasy
    # Calculate precision, recall and f1_score for each class
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1_score = 2 * precision * recall / (precision + recall)

    weights = np.repeat(np.sum(matrix, axis=1), 3).reshape(3, 5)
    macro_avg = np.mean([precision, recall, f1_score], axis=1)
    weighted_avg = np.average(np.array([precision, recall, f1_score]), weights=weights, axis=1)
    micro_TP = np.sum(TP)
    micro_FP = np.sum(FP)
    micro_FN = np.sum(FN)
    micro_precision = micro_TP / (micro_TP + micro_FP)
    micro_recall = micro_TP / (micro_TP + micro_FN)
    micro_f1_score = 2 * micro_precision * micro_recall / (micro_precision + micro_recall)
    micro_avg = np.array([micro_precision, micro_recall, micro_f1_score])
    accuracy = np.sum(TP) / np.sum(matrix)

    print("TP:", TP)
    print("FP:", FP)
    print("FN:", FN)
    print("f1 score:", f1_score)
    print("recall:", recall)
    print("precision:", precision)
    print("Macro avg:", macro_avg)
    print("Weighted avg:", weighted_avg)
    print("Micro TP:", micro_TP)
    print("Micro FP:", micro_FP)
    print("Micro FN:", micro_FN)
    print("Micro precision:", micro_precision)
    print("Micro recall:", micro_recall)
    print("Micro f1 score:", micro_f1_score)
    print("Micro avarage:", micro_avg)
    print("Accuracy:", accuracy)


if __name__ == "__main__":
    main()
