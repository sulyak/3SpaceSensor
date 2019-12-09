from datetime import datetime as dt

def parse_to_query(row):
    while len(row) < 153:
        row.append(-99)

    row = map(PrettyFloat, row)
    row_data = ""
    for i, str_data in enumerate(row):
        if i:
            row_data += ", "
        row_data += str(str_data) + " "
            
    # print(row_data)
    query = "insert into data values('%s', %s)" % (dt.now(), row_data)
    # print(query)
    return query

class PrettyFloat(float):
    def __repr__(self):
        return "%0.2f" % self

    def __str__(self):
        return self.__repr__()