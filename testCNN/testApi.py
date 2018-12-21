import pandas as pd
import pickle

def load_database_encoding():
    with open("encodedImageData" + '.pkl', 'rb') as f:
        return pickle.load(f)


# database = load_database_encoding()
# df = pd.DataFrame.from_dict(database)
# df.to_csv("my_att.csv")
# df1 = pd.read_csv('my_marked_attendance.csv')
# print(df1.head(5))
fp = open('time-sheet.log','a')
fp.write("Hello Archit")
fp.flush()


fp.write("Hello Archit")


fp.write("Hello Archit")


fp.write("Hello Archit")


fp.write("Hello Archit")


fp.write("Hello Archit")


fp.write("Hello Archit")


fp.write("Hello Archit")






