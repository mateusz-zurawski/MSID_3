# --------------------------------------------------------------------------
# ------------  Metody Systemowe i Decyzyjne w Informatyce  ----------------
# --------------------------------------------------------------------------
#  Zadanie 3: Regresja logistyczna
#  autorzy: A. Gonczarek, J. Kaczmar, S. Zareba, P. Dąbrowski
#  2019
# --------------------------------------------------------------------------

import numpy as np


def sigmoid(x):
    """
    Wylicz wartość funkcji sigmoidalnej dla punktów *x*.

    :param x: wektor wartości *x* do zaaplikowania funkcji sigmoidalnej Nx1
    :return: wektor wartości funkcji sigmoidalnej dla wartości *x* Nx1
    """
    return 1/(1 + np.exp(-x))


def logistic_cost_function(w, x_train, y_train):
    """
    Wylicz wartość funkcji logistycznej oraz jej gradient po parametrach.

    :param w: wektor parametrów modelu Mx1
    :param x_train: zbiór danych treningowych NxM
    :param y_train: etykiety klas dla danych treningowych Nx1
    :return: krotka (log, grad), gdzie *log* to wartość funkcji logistycznej,
        a *grad* jej gradient po parametrach *w* Mx1
    """
    N = y_train.shape[0]
    sigma = sigmoid(x_train@w)
    cost = y_train*(np.log(sigma)) + (1-y_train)*(np.log(1-sigma))
    log = (-1/N)*np.sum(cost)
    grad = (x_train.T @ (sigma - y_train)) / N
    return log, grad


def gradient_descent(obj_fun, w0, epochs, eta):
    """
    Dokonaj *epochs* aktualizacji parametrów modelu metodą algorytmu gradientu
    prostego, korzystając z kroku uczenia *eta* i zaczynając od parametrów *w0*.
    Wylicz wartość funkcji celu *obj_fun* w każdej iteracji. Wyznacz wartość
    parametrów modelu w ostatniej epoce.

    :param obj_fun: optymalizowana funkcja celu, przyjmująca jako argument
        wektor parametrów *w* [wywołanie *val, grad = obj_fun(w)*]
    :param w0: początkowy wektor parametrów *w* Mx1
    :param epochs: liczba epok algorytmu gradientu prostego
    :param eta: krok uczenia
    :return: krotka (w, log_values), gdzie *w* to znaleziony optymalny
        punkt *w*, a *log_values* to lista wartości funkcji celu w każdej
        epoce (lista o długości *epochs*)
    """
    values = []
    w = w0
    grad = obj_fun(w)[1]
    for i in range(epochs):
        w = w - (eta*grad)
        act_val, grad = obj_fun(w)
        values.append(act_val)
    values = np.array(values)
    return w, values.T


def stochastic_gradient_descent(obj_fun, x_train, y_train, w0, epochs, eta, mini_batch):
    """
    Dokonaj *epochs* aktualizacji parametrów modelu metodą stochastycznego
    algorytmu gradientu prostego, korzystając z kroku uczenia *eta*, paczek
    danych o rozmiarze *mini_batch* i zaczynając od parametrów *w0*. Wylicz
    wartość funkcji celu *obj_fun* w każdej iteracji. Wyznacz wartość parametrów
    modelu w ostatniej epoce.

    :param obj_fun: optymalizowana funkcja celu, przyjmująca jako argumenty
        wektor parametrów *w*, paczkę danych składających się z danych
        treningowych *x* i odpowiadających im etykiet *y*
        [wywołanie *val, grad = obj_fun(w, x, y)*]
    :param w0: początkowy wektor parametrów *w* Mx1
    :param epochs: liczba epok stochastycznego algorytmu gradientu prostego
    :param eta: krok uczenia
    :param mini_batch: rozmiar paczki danych / mini-batcha
    :return: krotka (w, log_values), gdzie *w* to znaleziony optymalny
        punkt *w*, a *log_values* to lista wartości funkcji celu dla całego
        zbioru treningowego w każdej epoce (lista o długości *epochs*)
    """

    w = w0
    values = []
    for k in range(epochs):
        for m in range(int(x_train.shape[0] / mini_batch)):
            grad = obj_fun(w, x_train[m * mini_batch: (m + 1) * mini_batch], y_train[m * mini_batch: (m + 1) * mini_batch])[1]
            w = w - (eta * grad)
        val = obj_fun(w, x_train, y_train)[0]
        values.append(val)
    values = np.array(values)
    return w, values.T


def regularized_logistic_cost_function(w, x_train, y_train, regularization_lambda):
    """
    Wylicz wartość funkcji logistycznej z regularyzacją l2 oraz jej gradient
    po parametrach.

    :param w: wektor parametrów modelu Mx1
    :param x_train: zbiór danych treningowych NxM
    :param y_train: etykiety klas dla danych treningowych Nx1
    :param regularization_lambda: parametr regularyzacji l2
    :return: krotka (log, grad), gdzie *log* to wartość funkcji logistycznej
        z regularyzacją l2, a *grad* jej gradient po parametrach *w* Mx1
    """
    log, grad = logistic_cost_function(w, x_train, y_train)
    log += regularization_lambda*0.5*np.sum(w[1:]**2)
    grad[1:] = np.add(grad[1:], regularization_lambda*w[1:])

    return log, grad

def prediction(x, w, theta):
    """
    Wylicz wartości predykowanych etykiet dla obserwacji *x*, korzystając
    z modelu o parametrach *w* i progu klasyfikacji *theta*.

    :param x: macierz obserwacji NxM
    :param w: wektor parametrów modelu Mx1
    :param theta: próg klasyfikacji z przedziału [0,1]
    :return: wektor predykowanych etykiet ze zbioru {0, 1} Nx1
    """
    y = []
    sigma = sigmoid(x@w)
    for sig in sigma:
        y.append(sig>theta)
    y = np.array(y)
    return y


def f_measure(y_true, y_pred):
    """
    Wylicz wartość miary F (F-measure) dla zadanych rzeczywistych etykiet
    *y_true* i odpowiadających im predykowanych etykiet *y_pred*.

    :param y_true: wektor rzeczywistych etykiet Nx1
    :param y_pred: wektor etykiet predykowanych przed model Nx1
    :return: wartość miary F (F-measure)
    """
    tp = 0
    fp = 0
    fn = 0
    for i in range(y_true.shape[0]):
        if y_true[i]==1 and y_pred[i]==1:
            tp +=1
        if y_pred[i]==0 and y_true[i]==1:
            fn +=1
        if y_pred[i]==1 and y_true[i]==0:
            fp +=1
    return (2*tp)/((2*tp)+fp+fn)


def model_selection(x_train, y_train, x_val, y_val, w0, epochs, eta, mini_batch, lambdas, thetas):
    """
    Policz wartość miary F dla wszystkich kombinacji wartości regularyzacji
    *lambda* i progu klasyfikacji *theta. Wyznacz parametry *w* dla modelu
    z regularyzacją l2, który najlepiej generalizuje dane, tj. daje najmniejszy
    błąd na ciągu walidacyjnym.

    :param x_train: zbiór danych treningowych NxM
    :param y_train: etykiety klas dla danych treningowych Nx1
    :param x_val: zbiór danych walidacyjnych NxM
    :param y_val: etykiety klas dla danych walidacyjnych Nx1
    :param w0: początkowy wektor parametrów *w* Mx1
    :param epochs: liczba epok stochastycznego algorytmu gradientu prostego
    :param eta: krok uczenia
    :param mini_batch: rozmiar paczki danych / mini-batcha
    :param lambdas: lista wartości parametru regularyzacji l2 *lambda*,
        które mają być sprawdzone
    :param thetas: lista wartości progów klasyfikacji *theta*,
        które mają być sprawdzone
    :return: krotka (regularization_lambda, theta, w, F), gdzie
        *regularization_lambda* to wartość regularyzacji *lambda* dla
        najlepszego modelu, *theta* to najlepszy próg klasyfikacji,
        *w* to parametry najlepszego modelu, a *F* to macierz wartości miary F
        dla wszystkich par *(lambda, theta)* #lambda x #theta
    """
    best_measure = 0
    best_lambda = lambdas[0]
    best_theta = thetas[0]
    best_w = w0
    F = []
    for l in lambdas:
        fun = lambda w,x_train,y_train: regularized_logistic_cost_function(w, x_train, y_train, l)
        w = stochastic_gradient_descent(fun, x_train, y_train, w0, epochs, eta, mini_batch)[0]
        for theta in thetas:
            act_measure = f_measure(y_val, prediction(x_val, w, theta))
            F.append(act_measure)
            if act_measure>best_measure:
                best_measure = act_measure
                best_lambda = l
                best_theta = theta
                best_w = w
    F = np.array(F).reshape(len(lambdas),len(thetas))
    return best_lambda, best_theta, best_w, F