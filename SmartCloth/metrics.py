import numpy as np
import pdb
import matplotlib.pyplot as plt

'''
 probs: result probs
labels: +1: positive case; -1: negative case
'''
def calc_rate(probs, labels):
    # step 0: check the input parameters
    if len(probs) != len(labels):
        print('The length of probs does not match with that of labels')
        return [], [], []

    # step 1: calc the number of positive and negative in ground labels
    '''
    num_gnd_pos + num_gnd_neg = len(labels)
    num_gnd_pos - num_gnd_neg = sum(labels)
    '''
    num_gnd_neg = len(labels)
    num_gnd_pos = (sum(labels) + num_gnd_neg) / 2
    num_gnd_neg = num_gnd_neg - num_gnd_pos
    if num_gnd_neg == 0 or num_gnd_pos == 0:
        print('num_gnd_neg={0},num_gnd_pos={1}'.format(num_gnd_neg, num_gnd_pos))
        return [], [], []

    # step 2: sort the probs inversely and so on
    '''
             |    GroundTruth 
    Predicted -----------------------
             | Positive | Negative
    ---------------------------------
    Positive |    TP    |    FP
    ---------------------------------
    Negative |    FN    |    TN
    ---------------------------------
    '''
    z = sorted(zip(probs, labels), key=lambda x: x[0], reverse=True)
    tp = 0.0
    fn = num_gnd_pos - tp
    fp = 0.0
    tn = num_gnd_neg - fp
    num_pre_pos = 0.0
    tpr = []
    fpr = []
    pre = []
    for item in z:
        if item[1] == 1:
            tp += 1.0
            fn -= 1.0
        else:
            fp += 1.0
            tn -= 1.0
        num_pre_pos += 1.0
        tpr.append(tp / num_gnd_pos)
        fpr.append(fp / num_gnd_neg)
        pre.append(tp / num_pre_pos)
    return tpr, fpr, pre

def calc_auc(fpr, tpr):
    auc = 0.0
    lst_x = 0.0
    for x, y in zip(fpr, tpr):
        if x != lst_x:
            auc += (x - lst_x) * y
            lst_x = x
    return auc

if __name__ == '__main__':
    n_case = 100
    nClass = 10
    labels = np.random.randint(0, nClass, size=n_case)
    probs = np.random.rand(n_case, nClass)
    probs_sum = probs.sum(axis=1)
    probs_tile = np.tile(probs_sum, (nClass, 1))
    probs_new = probs / np.transpose(probs_tile)
    for i in range(nClass):
        labels_ = [(item == i) * 2 - 1 for item in labels.tolist()]
        probs_ = probs[:, i].tolist()
        tpr, fpr, pre = calc_rate(probs_, labels_)
        plt.subplot(121)
        plt.plot(fpr, tpr)
        plt.subplot(122)
        plt.plot(tpr, pre)
        plt.show()
        pdb.set_trace()