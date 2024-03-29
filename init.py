import pickle
datalist=[["me","123","2"]]
with open("data.pkl", "wb") as file:
    pickle.dump(datalist, file)
with open("data.pkl","rb") as file:
    data=pickle.load(file)
    data.append(["pranav","2005","2"])
with open("data.pkl","wb") as file:
    pickle.dump(data,file)
