# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 14:31:06 2018

@author: sijian.xuan
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import auc,roc_curve, precision_recall_curve



def ROC(n_classes, y_score, y_test2): 
    ### Create ROC 
    fig=plt.figure(figsize=(10, 6))
    ax=fig.add_subplot(1,1,1)
    fpr = dict()
    tpr = dict()
    roc_auc=dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(np.array(y_test2)[:, i],y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
        ax.plot(fpr[i],tpr[i],label="target=%s, auc=%0.2f"%(i,roc_auc[i]))
        #ax.plot(fpr[i],tpr[i],label="target=%s, indication=%s"%(i,y_test2.columns[i]))
    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC")
    ax.legend(loc="lower right")
    ax.set_xlim(0,1.1)
    ax.set_ylim(0,1.1)
    ax.grid()
    plt.show()
    
def PRC(n_classes,y_test2,y_score):
    # precision_recall_curve
    ### obtain P-R
    fig=plt.figure(figsize=(10, 6))
    ax=fig.add_subplot(1,1,1)
    precision = dict()
    recall = dict()
    for i in range(n_classes):
        precision[i], recall[i], _ = precision_recall_curve(np.array(y_test2)[:, i],y_score[:, i])
        ax.plot(recall[i],precision[i],label="target=%s"%i)
    ax.set_xlabel("Recall Score")
    ax.set_ylabel("Precision Score")
    ax.set_title("Precision and Recall Curve")
    ax.legend(loc='best')
    ax.set_xlim(0,1.1)
    ax.set_ylim(0,1.1)
    ax.grid()
    plt.show()
    
    
def AUC_model2(best_clf, X_train, y_train, X_test, y_test, n_classes):
    from Multi_AUC import multi_auc,multi_a_value
    #Compute AUC for multi-classes 
    clf = best_clf
    model = clf.fit(X_train, y_train)
    y_pred_str= model.predict(X_test)
    y_pred_num = pd.DataFrame(data = y_pred_str, columns = ['y'])
    y_pred_num['y'] = y_pred_num['y'].astype('category')
    y_pred_num['y'] = y_pred_num['y'].cat.codes
    
    y_test_num = y_test
    y_test_num = y_test_num.astype('category')
    y_test_num = y_test_num.cat.codes
    
    res_base = pd.DataFrame(data = y_pred_str, columns = ['indication'])
    res_prob = model.predict_proba(X_test)
    res_base['prob_Derma'] = res_prob[:,0]
    res_base['prob_Gastro'] = res_prob[:,1]
    res_base['prob_Kinder'] = res_prob[:,2]
    res_base['prob_Ogen'] = res_prob[:,3]
    res_base['prob_Rheuma'] = res_prob[:,4]
    
    y_pred_list = y_pred_num['y'].tolist()
    l = [[y_pred_list[0],res_prob[0,:]]]
    for i in range(1, len(y_test)):
        l.append([y_pred_list[i],res_prob[i,:]])
    avalue = multi_a_value(l) 
    auc = multi_auc(data = l, num_classes = n_classes)
    print('The AUC of Model \n' + str(model) + '\n' + 'is: ' + str(auc))




def AUC_model3(best_clf, X_train, y_train, X_test, y_test, n_classes):
    from Multi_AUC import multi_auc,multi_a_value
    # Overall ROC

    #Compute AUC for multi-classes 
    clf = best_clf
    model = clf.fit(X_train, y_train)
    y_pred_str= model.predict(X_test)
    y_pred_num = pd.DataFrame(data = y_pred_str, columns = ['y'])
    y_pred_num['y'] = y_pred_num['y'].astype('category')
    y_pred_num['y'] = y_pred_num['y'].cat.codes

    y_test_num = y_test
    y_test_num = y_test_num.astype('category')
    y_test_num = y_test_num.cat.codes

    res_base = pd.DataFrame(data = y_pred_str, columns = ['indication'])
    res_prob = model.predict_proba(X_test)
    res_base['prob_AS'] = res_prob[:,0]
    res_base['prob_PsA'] = res_prob[:,1]
    res_base['prob_RA'] = res_prob[:,2]

    y_pred_list = y_pred_num['y'].tolist()
    l = [[y_pred_list[0],res_prob[0,:]]]
    for i in range(1, len(y_test)):
        l.append([y_pred_list[i],res_prob[i,:]])
    avalue = multi_a_value(l)
    
    auc = multi_auc(data = l, num_classes = n_classes)
    print('The AUC of Model \n' + str(model) + '\n' + 'is: ' + str(auc))
