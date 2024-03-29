import pickle
with open("data.pkl", "rb") as file:
    data=pickle.load(file)
for i in data:
    for j in i:
        print(j,end=" ")
    print()