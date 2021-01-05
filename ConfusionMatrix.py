class confusionMatrix:
    """
    date: Mar 16, 2018
    This class aims to create confusion Matrix which has a similar style 
    in R (caret::confusionMatrix())    
    
    !!!! PLEASE NOTICE !!!!
    The first argument is the predicted values;
    The second argument is the actual values. 
    This is consistent with caret::confusionMatrix() in R,
    and opposite to confusion_matrix() in sklearn.
    
    .show() will print the results
    .result is a dictionary containing key information of the confusion matrix.
    """
    def __init__(self, predicted, actual):
        from sklearn.metrics import confusion_matrix
        import pandas as pd
        import numpy as np
        label = sorted(list(actual.value_counts().index))
        l = len(label)
        cfm = confusion_matrix(actual, predicted, labels = label)
        cfm = pd.DataFrame(cfm.T, columns = label, 
                           index = ['      ' + str(i) for i in label])
        precision = np.zeros(l)
        Recall = np.zeros(l)
        right = 0
        for i in range(l):
            precision[i] = (cfm.iloc[i,i] / sum(cfm.iloc[i,:]))
            Recall[i] = (cfm.iloc[i,i] / sum(cfm.iloc[:,i]))
            right = right + cfm.iloc[i,i]
            
        cfmStatistics = np.vstack((pd.DataFrame(precision).T,
                                   pd.DataFrame(Recall).T))
        cfmStatistics = pd.DataFrame(cfmStatistics, 
                                     columns = label,
                                     index = ['Precision','Recall'])
        Accuracy = round(right / sum(sum(np.array(cfm))), 4)
        NIR = round(max(actual.value_counts()) / sum(sum(np.array(cfm))), 4)
        self.result = {'cfm':cfm, 'Accuracy':Accuracy, 
                                  'NIR':NIR, 'Statistics':cfmStatistics}
        
    def show(self):
        print('Confusion Matrix and Statistics\n')
        print('           Reference')
        print('Prediction')
        print(self.result['cfm'], '\n')
        print('Overall Statistics\n')
        print('              Accuracy : ', self.result['Accuracy'])
        print('   No Information Rate : ', self.result['NIR'], '\n')        
        print('Statistics by Class:\n')
        print(self.result['Statistics'])
        

def nearZeroVar(raw2, freqCut = 99/1, uniqueCut = 10):
    """
    This function is similar with the one in R (caret::nearZeroVar) with fewer
    Arguments.
    
    
    Description
    
    nearZeroVar diagnoses predictors that have one unique value (i.e. are zero 
    variance predictors) or predictors that are have both of the following 
    characteristics: they have very few unique values relative to the number 
    of samples and the ratio of the frequency of the most common value to the 
    frequency of the second most common value is large.
    
    
    Arguments
    
    freqCut	: the cutoff for the ratio of the most common value to the 
              second most common value.
    uniqueCut : the cutoff for the percentage of distinct values out of 
              the number of total samples
    """
    import numpy as np
    uniqueCut_1 = uniqueCut / 100 # be consistent with nearZeroVar in R(caret)
    n = raw2.columns
    todel = list()
    for col in n:
        if(raw2[col].dtypes == 'O'):
            if((list(raw2[col].value_counts())[0] / 
                list(raw2[col].value_counts())[1]) > freqCut):
                if(len(raw2[col].unique()) / len(raw2[col]) < uniqueCut_1):
                    todel.append(col)
                    continue
        else:
            if(np.var(raw2[col]) == 0):
                todel.append(col)
                continue
            if((list(raw2[col].value_counts())[0] / 
                list(raw2[col].value_counts())[1]) > freqCut):
                if(len(raw2[col].unique()) / len(raw2[col]) < uniqueCut_1):
                    todel.append(col)
                    continue
    return todel
      