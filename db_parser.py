from datetime import datetime as dt

def parse_to_query(row):
    np.set_printoptions(precision=2)
    # while len(row) < 27:
    #    row.append(-99)

    row = map(PrettyFloat, row)
    row_data = ""
    for i, str_data in enumerate(row):
        if i:
            row_data += ", "
        row_data += str(str_data) + " "
            
    # print(row_data)
    return "insert into data values(%s, '%s')" % (dt.now(), row_data)

class PrettyFloat(float):
    def __repr__(self):
        return "%0.2f" % self

    def __str__(self):
        return self.__repr__()