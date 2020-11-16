#!/usr/bin/python
# -*- coding: latin-1 -*-

### LOAD LIBRARIES
import pandas as pd
import re
import string
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import roc_curve, auc
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
import pickle
from tqdm import tqdm

### GLOBAL VARIABLES
path_data = 'tmp/output'
path_out_model = 'data'
file_in_resuelve = "resuelve.csv"
file_out_model1  = 'ModelOrdenVivienda.pkl'
file_out_model2  = 'ModelProyectosProductivos.pkl'
file_out_model3  = 'ModelCompensacionVictimas.pkl'
file_out_model4  = 'ModelCompensacionTerceros.pkl'
file_out_model5  = 'ModelSegundosOcupantes.pkl'
file_out_model6  = 'ModelAlivioPredial.pkl'
file_out_model7  = 'ModelAlivioSPD.pkl'
file_out_model8  = 'ModelAlivioPasivosFinancieros.pkl'
file_out_model9  = 'ModelPagoCostas.pkl'
file_out_model10 = 'ModelAdministracionProyectosProductivos.pkl'
file_out_model11 = 'ModelOtros.pkl'
file_out_model12 = 'ModelDireccionSocial.pkl'
file_out_model13 = 'ModelCatastro.pkl'

### FUNCTIONS
#This function return metrics from confusion matrix
def confusionMetrics(ytest,ypred):
    tn, fp, fn, tp = confusion_matrix(ytest,ypred).ravel()
    # accuracy
    acc = (tn + tp)/(tn + fp + fn + tp)
    #Precision [positive predictive value]
    pre = tp/(tp+fp)
    #Recall [sensitivity, hit rate, or the true positive rate (TPR)]
    sen = tp/(tp+fn)
    # Specificity [true negative rate (TNR)]
    spe = tn/(tn+fp)
    #F1 score
    f1s = (2*tp)/(2*tp+fp+fn)
    return {'Accuracy':[acc], 'Precision':[pre], 'Sensitivity':[sen], 'Specificity':[spe], 'F1 score':[f1s]}
#This function trains six models and calculate metrics to compare between models
def models(trainX, testX, trainY, testY):
    output = []
    # NB
    nb = GaussianNB()
    nb.fit(trainX,trainY)
    y_pred=nb.predict(testX)
    df1 = confusionMetrics(testY,y_pred)
    df2 = pd.DataFrame.from_dict(df1)
    df2['Model'] = 'NB'
    output.append(df2)
    y_pred_probs = nb.predict_proba(testX)
    y_pred_probs = y_pred_probs[:, 1]
    roc_vs = roc_curve(test_y, y_pred_probs)
    auc_vs = auc( roc_vs[0], roc_vs[1] )
    df2['AUC'] = auc_vs
    # SVM
    svc = LinearSVC(C = 1)
    svc.fit(trainX,trainY)
    y_pred=svc.predict(testX)
    df1 = confusionMetrics(testY,y_pred)
    df2 = pd.DataFrame.from_dict(df1)
    df2['Model'] = 'SVM'
    output.append(df2)
    # Random Forest
    rf = RandomForestClassifier(n_estimators = 50, random_state=42)
    rf.fit(trainX,trainY)
    y_pred=rf.predict(testX)
    df1 = confusionMetrics(testY,y_pred)
    df2 = pd.DataFrame.from_dict(df1)
    df2['Model'] = 'Random Forest'
    y_pred_probs = rf.predict_proba(testX)
    y_pred_probs = y_pred_probs[:, 1]
    roc_vs = roc_curve(test_y, y_pred_probs)
    auc_vs = auc( roc_vs[0], roc_vs[1] )
    df2['AUC'] = auc_vs
    output.append(df2)
    # Bagging meta-estimator
    bagging = BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5)
    bagging.fit(trainX, trainY)
    y_pred = bagging.predict(testX)
    df1 = confusionMetrics(testY,y_pred)
    df2 = pd.DataFrame.from_dict(df1)
    df2['Model'] = 'Bagging meta-estimator'
    y_pred_probs = bagging.predict_proba(testX)
    y_pred_probs = y_pred_probs[:, 1]
    roc_vs = roc_curve(test_y, y_pred_probs)
    auc_vs = auc( roc_vs[0], roc_vs[1] )
    df2['AUC'] = auc_vs
    output.append(df2)
    # Gradient Boosting Classifier
    gradient = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0).fit(train_x, train_y)
    y_pred = gradient.predict(testX)
    df1 = confusionMetrics(testY,y_pred)
    df2 = pd.DataFrame.from_dict(df1)
    df2['Model'] = 'Gradient Boosting Classifier'
    y_pred_probs = gradient.predict_proba(testX)
    y_pred_probs = y_pred_probs[:, 1]
    roc_vs = roc_curve(test_y, y_pred_probs)
    auc_vs = auc( roc_vs[0], roc_vs[1] )
    df2['AUC'] = auc_vs
    output.append(df2)
    # Neural Networks
    nn = MLPClassifier(hidden_layer_sizes=(500, 250), learning_rate='adaptive', max_iter=2000, random_state=21)
    nn.fit(trainX, trainY)
    y_pred = nn.predict(testX)
    df1 = confusionMetrics(testY,y_pred)
    df2 = pd.DataFrame.from_dict(df1)
    df2['Model'] = 'Neural Networks'
    y_pred_probs = nn.predict_proba(testX)
    y_pred_probs = y_pred_probs[:, 1]
    roc_vs = roc_curve(test_y, y_pred_probs)
    auc_vs = auc( roc_vs[0], roc_vs[1] )
    df2['AUC'] = auc_vs
    output.append(df2)
    return output, nn, gradient, bagging, rf, svc, nb

#This function save models to disc and then we can predict in sentences without classification
def model_save(dframe, model_name):
    df1 = dframe.head(1)
    if( (df1['Model'] == 'Gradient Boosting Classifier')[0] ):
        model = gradient
    if( (df1['Model'] == 'Neural Networks')[0] ):
        model = nn
    if( (df1['Model'] == 'Random Forest')[0] ):
        model = rf
    if( (df1['Model'] == 'Bagging meta-estimator')[0] ):
        model = bagging
    if( (df1['Model'] == 'SVM')[0] ):
        model = svc
    if( (df1['Model'] == 'NB')[0] ):
        model = nb
    pkl_filename = model_name
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)

### EXECUTION
resuelve_e = pd.read_csv(path_data + '/' + file_in_resuelve)
stopwords_spanish = stopwords.words('spanish')
resuelve_e['RE'] = ''
for r in tqdm(range(len(resuelve_e))):
    text_temp = resuelve_e['Resuelve'][r]
    text_temp = re.sub(r'C.C.', r'CÉDULA', text_temp)
    text_temp = re.sub(r'No.', r'NÚMERO', text_temp)
    text_temp = sent_tokenize(text_temp.lower())
    text_temp2 = []
    for sentence in range(len(text_temp)):
        ou1 = ""
        for word in word_tokenize(text_temp[sentence]):
            if(word not in stopwords_spanish and word not in string.punctuation):
                ou1 += ' '+word
        text_temp2.append(ou1)
        ou2 = ""
        for sentence in text_temp2:
            ou2 += ' '+sentence
            resuelve_e['RE'][r] = ou2

#Model 1 (ORDEN DE VIVIENDA)
resuelve_e['Y'] = np.where(resuelve_e['ORDEN DE VIVIENDA']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model1)

#Model 2 (PROYECTOS PRODUCTIVOS PARA BENEFICIARIOS DE RESTITUCIÓN)
resuelve_e['Y'] = np.where(resuelve_e['PROYECTOS PRODUCTIVOS PARA BENEFICIARIOS DE RESTITUCIÓN']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model2)

#Model 3 (COMPENSACIÓN VICTIMAS)
resuelve_e['Y'] = np.where(resuelve_e['COMPENSACIÓN VICTIMAS']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model3)

#Model 4 (COMPENSACIÓN TERCEROS)
resuelve_e['Y'] = np.where(resuelve_e['COMPENSACIÓN TERCEROS']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model4)

#Model 5 (SEGUNDOS OCUPANTES)
resuelve_e['Y'] = np.where(resuelve_e['SEGUNDOS OCUPANTES']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model5)

#Model 6 (ALIVIO PREDIAL)
resuelve_e['Y'] = np.where(resuelve_e['ALIVIO PREDIAL']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model6)

#Model 7 (ALIVIO DE SERVICIOS PÚBLICOS)
resuelve_e['Y'] = np.where(resuelve_e['ALIVIO DE SERVICIOS PÚBLICOS']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model7)

#Model 8 (ALIVIO DE PASIVOS FINANCIEROS)
resuelve_e['Y'] = np.where(resuelve_e['ALIVIO DE PASIVOS FINANCIEROS']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model8)

#Model 9 (PAGOS DE COSTAS Y GASTOS JUDICIALES)
resuelve_e['Y'] = np.where(resuelve_e['PAGOS DE COSTAS Y GASTOS JUDICIALES']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model9)

#Model 10 (ADMINISTRACIÓN PROYECTOS PRODUCTIVOS AGROINDUSTRIALES)
resuelve_e['Y'] = np.where(resuelve_e['ADMINISTRACIÓN PROYECTOS PRODUCTIVOS AGROINDUSTRIALES']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model10)

#Model 11 (OTRAS ÓRDENES)
resuelve_e['Y'] = np.where(resuelve_e['OTRAS ÓRDENES']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model11)

#Model 12 (ORDENES A DIRECCIÓN SOCIAL)
resuelve_e['Y'] = np.where(resuelve_e['ORDENES A DIRECCIÓN SOCIAL']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model12)

#Model 13 (ORDENES CATASTRALES)
resuelve_e['Y'] = np.where(resuelve_e['ORDENES CATASTRALES']== 'SI', 1, 0)
print(resuelve_e['Y'].value_counts(dropna=False, sort=True))
list_text = list(resuelve_e['RE'].values)
outputY   = resuelve_e['Y'].values
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
all_words      = count_vector.get_feature_names()
x = matrix_text_cv.toarray()
y = outputY
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
table_summary_models, nn, gradient, bagging, rf, svc, nb = models(train_x, test_x, train_y, test_y)
DF = pd.concat(table_summary_models)
DF.sort_values(by=["F1 score"],ascending=False,inplace=True)
model_save(dframe = DF, model_name = path_out_model + '/' + file_out_model13)