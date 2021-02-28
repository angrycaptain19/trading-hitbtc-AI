from itertools import combinations
import pandas as pd
import matplotlib.pyplot as plt
from keras.utils.np_utils import to_categorical


jim = len([komb for komb in combinations(
    [karte for karte in range(52)],5)])
#print(jim)

train = pd.read_csv("poker-hand-training-true.csv",
                    header=None,
                    names=["S1","C1","S2","C2","S3","C3","S4","C4","S5","C5","hand"])
print(train.sample(10))
train.hand.value_counts(normalize=True)
train.hand.value_counts(normalize=True).plot(kind="bar")
plt.xlabel("Hand")
plt.ylabel("Relative Häufigkeit")
#plt.show()
X = train.drop("hand",axis=1).values
y = train.hand.values
dummy_y = to_categorical(y)
print(dummy_y[:20])