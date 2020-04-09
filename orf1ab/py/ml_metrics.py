import matplotlib.pyplot as plt
import numpy as np
import itertools
import sklearn


def plot_confusion_matrix(cm, class_names,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def evaluate_model(predictions, ytest, class_dict):
    '''
    predictions: List of predicted labels
    ytest: Embedding matrix, test data
    class_dict: {str:int}
    Prints F1 score and confusion matrix
    '''
    y_pred = []
    for i in predictions:
        y_pred.append(i.argmax())

    # print('F1 Score: ',sklearn.metrics.f1_score(ytest, y_pred, average='weighted'))
    # print('Accuracy:', sklearn.metrics.accuracy_score(ytest, y_pred))
    print(f'Multiclass log loss: {multiclass_logloss(ytest, predictions)}')
    class_names = class_dict.values()
    print(class_names)
    cnf_matrix = sklearn.metrics.confusion_matrix(ytest, y_pred)
    np.set_printoptions(precision=2)

    # Plot non-normalized confusion matrix
    plt.figure(figsize=(9, 9))
    plot_confusion_matrix(cnf_matrix, class_names, True,
                          title='Confusion matrix, with normalization')
    plt.show()

def multiclass_logloss(actual, predicted, eps=1e-15):
    """Multi class version of Logarithmic Loss metric.
    :param actual: Array containing the actual target classes
    :param predicted: Matrix with class predictions, one probability per class
    """
    # Convert 'actual' to a binary array if it's not already:
    if len(actual.shape) == 1:
        actual2 = np.zeros((actual.shape[0], predicted.shape[1]))
        for i, val in enumerate(actual):
            actual2[i, val] = 1
        actual = actual2

    clip = np.clip(predicted, eps, 1 - eps)
    rows = actual.shape[0]
    vsota = np.sum(actual * np.log(clip))
    return -1.0 / rows * vsota
