import pandas as pd
import numpy as np

# csvファイルからデータフレーム形式でデータを読み込む
train = pd.read_csv("./assets/train.csv")
test = pd.read_csv("./assets/test.csv")

# データフレームの先頭5行を表示
print(train.head())
print(test.head())

test_shape = test.shape
train_shape = train.shape

# データフレームの行数と列数を表示
print(train_shape)
print(test_shape)

# データフレームの情報を表示
print(train.describe())
print(test.describe())

# 欠損値の割合を計算する関数
def kesson_table(df):
    null_val = df.isnull().sum()
    percent = 100 * df.isnull().sum() / len(df)
    kesson_table = pd.concat([null_val, percent], axis=1)
    kesson_table_ren_columns = kesson_table.rename(
        columns={0: '欠損数', 1: '%'})
    return kesson_table_ren_columns


print("訓練データの欠損情報")
print(kesson_table(train))
print("テストデータの欠損情報")
print(kesson_table(test))

# 欠損値を補完する
train["Age"] = train["Age"].fillna(train["Age"].median())
train["Embarked"] = train["Embarked"].fillna("S")

print("訓練データの欠損情報: 補完後")
print(kesson_table(train))

# 欠損値を補完する
train["Age"] = train["Age"].fillna(train["Age"].median())
train["Embarked"] = train["Embarked"].fillna("S")

print("訓練データの欠損情報: 補完後")
print(kesson_table(train))

# 文字列を数値に変換
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