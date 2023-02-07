import pandas as pd;
y=[{
    "color": "purple",
    "type": "minivan",
    "capacity": 7
  },
  {
    "color": "red",
    "type": "station wagon",
    "capacity": 5
  }]
x=pd.DataFrame(y)
z=pd.Series(y)
# print(x)
print(z)

# convert dataframe to numpy array
# arr = df.to_numpy()
stack=list();
for dd in z:
    print(dd)
    if(len(stack)>0):
        c=[x for x in stack if x['capacity'] == 5]
        # c=stack.find(car => car['capacity'] === 5);
        if len(c) == 0 :
            stack.append(dd)
        print(len(c) > 0 and 'it exist' or 'Not exist');
    else:
        stack.append(dd)
print(stack)
