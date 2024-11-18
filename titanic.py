import pandas as pd
import numpy as np
from sklearn import tree

# csvファイルからデータフレーム形式でデータを読み込む
train = pd.read_csv("./assets/train.csv")
test = pd.read_csv("./assets/test.csv")

# データフレームの先頭5行を表示
# print(train.head())
# print(test.head())

test_shape = test.shape
train_shape = train.shape

# データフレームの行数と列数を表示
# print(train_shape)
# print(test_shape)

# データフレームの情報を表示
# print(train.describe())
# print(test.describe())

# 欠損値の割合を計算する関数
def kesson_table(df):
    null_val = df.isnull().sum()
    percent = 100 * df.isnull().sum() / len(df)
    kesson_table = pd.concat([null_val, percent], axis=1)
    kesson_table_ren_columns = kesson_table.rename(
        columns={0: '欠損数', 1: '%'})
    return kesson_table_ren_columns


# print("訓練データの欠損情報")
# print(kesson_table(train))
# print("テストデータの欠損情報")
# print(kesson_table(test))

# 欠損値を補完する
train["Age"] = train["Age"].fillna(train["Age"].median())
train["Embarked"] = train["Embarked"].fillna("S")

# print("訓練データの欠損情報: 補完後")
# print(kesson_table(train))


# 文字列を数値に変換(train)
# train["Sex"][train["Sex"] == "male"] = 0
# train["Sex"][train["Sex"] == "female"] = 1
# train["Embarked"][train["Embarked"] == "S" ] = 0
# train["Embarked"][train["Embarked"] == "C" ] = 1
# train["Embarked"][train["Embarked"] == "Q"] = 2

train.loc[train["Sex"] == "male", "Sex"] = 0
train.loc[train["Sex"] == "female", "Sex"] = 1
train.loc[train["Embarked"] == "S", "Embarked"] = 0
train.loc[train["Embarked"] == "C", "Embarked"] = 1
train.loc[train["Embarked"] == "Q", "Embarked"] = 2


print("訓練データの先頭10行 : 文字列を数値に変換後")
print(train.head(10))

# 文字列を数値に変換(test)
test["Age"] = test["Age"].fillna(test["Age"].median())
test.loc[test["Sex"] == "male", "Sex"] = 0
test.loc[test["Sex"] == "female", "Sex"] = 1
test.loc[test["Embarked"] == "S", "Embarked"] = 0
test.loc[test["Embarked"] == "C", "Embarked"] = 1
test.loc[test["Embarked"] == "Q", "Embarked"] = 2
test.loc[test["Fare"].isnull(), "Fare"] = test["Fare"].median()

# print("テストデータの欠損情報: 補完後")
# print(kesson_table(test))

print("テストデータの先頭10行 : 文字列を数値に変換後")
print(test.head(10))

# trainの目的変数と説明変数の値を取得
target = train["Survived"].values
features_one = train[["Pclass", "Sex", "Age", "Fare"]].values

# 決定木の作成
my_tree_one = tree.DecisionTreeClassifier()
my_tree_one = my_tree_one.fit(features_one, target)

# testの説明変数の値を取得
test_features = test[["Pclass", "Sex", "Age", "Fare"]].values

# testの説明変数を使ってmy_tree_oneのモデルで予測
my_prediction = my_tree_one.predict(test_features)

# 予測データを表示
print(my_prediction)

# PassengerIdを取得
PassengerId = np.array(test["PassengerId"]).astype(int)

# my_prediction(予測データ)とPassengerIdをデータフレームに落とし込む
my_solution = pd.DataFrame(my_prediction, PassengerId, columns=["Survived"])

# my_tree_one.csvとして書き出し
my_solution.to_csv("data/my_tree_one.csv", index_label=["PassengerId"])