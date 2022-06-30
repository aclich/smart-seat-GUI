import argparse
import os
import json
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from datetime import datetime
from libs.config import CLASS_MAP


BASE_PATH = os.path.dirname(__file__)

def gen_training_data(file_path: str, pred_all=False):
    file_list = os.listdir(file_path)
    data_list = []
    target_list = []
    for f in file_list:
        if not f.endswith('.json'):
            continue
        json_path = os.path.join(file_path, f)
        js = json.load(open(json_path))
        for d in js:
            x = np.array([*d['data'], int(d['gender']), float(d['height']), float(d['weight'])])
            y = int(d['sit_pos'])
            if pred_all:
                data_list.append(x)
                target_list.append({"ans":y, "name":f, "time": d['time']})
            else:
                data_list.append(x)
                target_list.append(y)
    # x_train, x_test, y_train, y_test =
    if data_list == []:
        print(f"no json file found in {file_path}!")
        raise FileNotFoundError(f"{file_path} 沒有json檔案!")
    
    if pred_all:
        return data_list, target_list
    else: 
        return train_test_split(data_list, target_list, test_size=0.5, random_state=4)


class classifier(object):
    def __init__(self):
        self.rf_cls = RandomForestClassifier()
        self.data_path = os.path.join(BASE_PATH, 'json')
        self.load_tree()
        

    def load_tree(self, file_name: str = ""):
        try:
            file_name = os.path.join(BASE_PATH, "./rf_predictor_last.joblib")
            self.loaded_tree = joblib.load(file_name)
        except FileNotFoundError as e:
            print(f"No trained RF model! {e}")

    def train(self, model: str):
        # data_path = os.path.join(BASE_PATH, 'json')
        x_train, x_test, y_train, y_test = gen_training_data(self.data_path)
        print(f"training count:{len(y_train)}, test count: {len(y_test)}")
        
        if model == "RF":
            self._train_RF(x_train, x_test, y_train, y_test)

        elif model == "DNN":
            self._train_DNN(x_train, x_test, y_train, y_test)

        else:
            print(f"Not supproted model: {model}")

    def _train_RF(self, x_train, x_test, y_train, y_test):
        self.rf_cls = RandomForestClassifier(n_estimators=50, n_jobs= -1, min_samples_leaf=25)
        self.rf_cls.fit(x_train, y_train)
        y_pred = self.rf_cls.predict(x_test)
        self._check_ans(y_pred, y_test)
        self._save_rf_model()
        

    def _train_DNN(self, x_train, x_test, y_train, y_test):
        print("還沒做拉")

    def _check_ans(self, y_pred, y_test):
        ans_sum =  sum([1 if p==t else 0 for p,t in zip(y_pred, y_test)])
        class_dict, acc = {}, 0
        for p,t in zip(y_pred, y_test):
            if t not in class_dict:
                class_dict[t] = [0,0]
            class_dict[t][1] += 1
            if p == t:
                class_dict[t][0] += 1
                acc += 1

        print(f"model result:\nacc/total: {acc}/{len(y_test)}, accuracy={acc/len(y_test)}")
        print(f"result of each class:")
        for c, ans in class_dict.items():
            print(f"{CLASS_MAP[c]}: acc/total: {ans[0]}/{ans[1]}, accuracy={ans[0]/ans[1]}")
        labels = [v for _,v in CLASS_MAP.items() ]
        y_test, y_pred = self._convert_label(y_test), self._convert_label(y_pred)
        print(" ".join(labels))
        print(metrics.confusion_matrix(y_test, y_pred, labels=labels))
        print(metrics.classification_report(y_test, y_pred, labels=labels))

    def _convert_label(self, y_list):
        return [CLASS_MAP[y] for y in y_list]

    def _save_rf_model(self):
        joblib.dump(self.rf_cls, os.path.join(BASE_PATH, f"./rf_predictor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.joblib"))
        joblib.dump(self.rf_cls, os.path.join(BASE_PATH, "./rf_predictor_last.joblib"))

    def predict(self, model, x, cvt_ch:bool=True):
        if model == "RF":
            return CLASS_MAP[self.loaded_tree.predict([x])[0]] if cvt_ch else self.loaded_tree.predict([x])[0]
        if model == "DNN":
            raise Exception("還沒做好")

    def predict_all(self, model="RF"):
        data_list, target_list = gen_training_data(file_path=self.data_path, pred_all=True)
        if model == "RF":
            self.load_tree()
            pred_list = self.loaded_tree.predict(data_list)
            for p, d in zip(pred_list, target_list):
                if p != d['ans']:
                    print(f"{d['name']}_{d['time']} pred:{CLASS_MAP[p]}, ans:{CLASS_MAP[d['ans']]}")
            self._check_ans(y_pred=pred_list, y_test=[d['ans'] for d in target_list])
        else:
            print("not support")
            pass