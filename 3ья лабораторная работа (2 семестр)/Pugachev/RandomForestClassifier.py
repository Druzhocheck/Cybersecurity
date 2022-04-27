from nfstream import NFStreamer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn import metrics
import numpy as np

def writedown(value):
    with open("RandomForestClassifier.md", "a", encoding="utf-8") as file:
        file.write(value)

if __name__ == '__main__':

    # загрузка датасета
    df = pd.concat([NFStreamer(source='DataSets/1/ipsec.pcap').to_pandas(columns_to_anonymize=[]),
                        NFStreamer(source='DataSets/1/openvpn.pcap').to_pandas(columns_to_anonymize=[]),
                        NFStreamer(source='DataSets/1/WireGuard.pcap').to_pandas(columns_to_anonymize=[]),
                        NFStreamer(source='DataSets/2/IPSec.pcap').to_pandas(columns_to_anonymize=[]),
                        NFStreamer(source='DataSets/2/openvpn.pcap').to_pandas(columns_to_anonymize=[]),
                        NFStreamer(source='DataSets/2/WireGuard-telemetry.pcap').to_pandas(columns_to_anonymize=[]),
                        NFStreamer(source='DataSets/3/clear.pcap').to_pandas(columns_to_anonymize=[]),
                        NFStreamer(source='DataSets/4/all.pcap').to_pandas(columns_to_anonymize=[])])
    # выходные данные 
    y = df ['application_category_name']

    # входные данные
    x = df[["src_port", "dst_port", "protocol","bidirectional_packets","bidirectional_bytes","application_name"]]

    # перевод в категориальные признаки
    x = pd.get_dummies(x[["src_port", "dst_port", "protocol","bidirectional_packets","bidirectional_bytes","application_name"]])

    # тренировка модели
    model = RandomForestClassifier(n_estimators=50, max_features=10, max_depth=10)
    x_train = x[0:int((len(x)/2))]
    y_train = y[0:int((len(x)/2))]
    model.fit(x_train, y_train)

    # предсказание
    x_test = x[int((len(x)/2)):len(x)]
    prediction = model.predict(x_test)
    y_test = y[int((len(x)/2)):len(x)]
    accuracy = metrics.accuracy_score(y_test, prediction)
    print("Accuracy:", accuracy)

    # Результат
    result = pd.DataFrame({"Real values": y_test,
                   "Predicton values": prediction})
    count = 0
    y_test = np.array(y_test)
    prediction = np.array(prediction)

    # посчет ошибок
    for i in range(len(prediction)):
        if y_test[i] != prediction[i]:
            count += 1
    with open("RandomForestClassifier.md", "w", encoding="utf-8") as file:
        file.write("Random Forest Classifier\n\n")
    writedown("Accuracy: " + str(accuracy)+'\n\n')
    writedown("Number of wrong predictions: {}/{}\n\n".format(count, int(len(x)/2)))
    writedown(result.to_markdown())