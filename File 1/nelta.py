"""
Add LabeledList and Table classes
"""



from ast import Try
from hashlib import new
from re import X
from tkinter.messagebox import NO
from typing import List
import csv


class LabeledList:
    def __init__(self, data=None, index=None):
        self.values=data
        self.index=index
        if index is None:
            ll = [(i, d) for i, d in enumerate(data)]
        else:
            if len(index) == len(data):
                ll = [(index[i], data[i]) for i in range(len(data))]
            else:
                print("Error: the length of data and the length of index are different.")
        self.ll=ll

    def __str__(self):
        result = ""
        for i, d in self.ll:
            result += f'{i:>10} {d:>10}\n'
        return result

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.values)

    def map(self, f):
        new_ll = list(map(f, self.values))
        return LabeledList(new_ll, self.index)

    def __getitem__(self, key_list):
        # If the key is a LabeledList
        if isinstance(key_list, LabeledList):
            new_ll = [(i, d) for i, d in self.ll if i in key_list.values]
            index, data = zip(*new_ll)
            return LabeledList(list(data), list(index))
        # If the key is a list
        elif isinstance(key_list, list):
            # If the key is a Boolean
            if isinstance(key_list[0], bool):
                new_ll = [(self.index[i], self.values[i]) for i in range(len(self.values)) if key_list[i] == True]
                index, data = zip(*new_ll)
                return LabeledList(list(data), list(index))
            else:
                new_ll=[(i, d) for i, d in self.ll if i in key_list]
                index, data = zip(*new_ll)
                return LabeledList(list(data), list(index))
        # If the key is str or int
        elif isinstance(key_list, str):
            new_ll = [(self.index[i], self.values[i]) for i in range(len(self.values)) if key_list[i] == key_list]
            if len(new_ll) == 1:
                return new_ll[0][1]
            else:
                index, data = zip(*new_ll)
                return LabeledList(list(data), list(index)) 
        elif isinstance(key_list, int):
                new_ll = [(self.index[i], self.values[i]) for i in range(len(self.values)) if key_list[i] == key_list]
                return new_ll[0][1]

    def __eq__(self, scalar):
        if scalar is None:
            return False
        else:
            new_ll = [(i, d == scalar) for i, d in self.ll]
            index, boo = zip(*new_ll)
            return LabeledList(list(boo), list(index))

    def __ne__(self, scalar):
        if scalar is None:
            return False
        else:
            new_ll = [(i, d != scalar) for i, d in self.ll]
            index, boo = zip(*new_ll)
            return LabeledList(list(boo), list(index))

    def __gt__(self, scalar):
        if scalar is None:
            return False
        else:
            new_ll = [(i, d > scalar) for i, d in self.ll]
            index, boo = zip(*new_ll)
            return LabeledList(list(boo), list(index))

    def __lt__(self, scalar):
        if scalar is None:
            return False
        else:
            new_ll = [(i, d < scalar) for i, d in self.ll]
            index, boo = zip(*new_ll)
            return LabeledList(list(boo), list(index))

class Table:
    def __init__(self, data, index=None, columns=None):
        self.values=data
        self.index=index
        self.columns=columns
        if index is None:
            self.index=list(range(len(self.values)))
        if columns is None:
            self.columns=[col for col in range(len(self.values[0]))]

    def __str__(self):
        max_col=[]
        for row in zip(self.columns, *self.values):
            max_len=len(str(max(row,key=lambda x: len(str(x)))))
            max_col.append(max_len)
        max_index=len(str(max(self.index, key=lambda x: len(str(x)))))
        result = ""
        # corner case and 1st row
        row=("{:>"+f"{max_index+2}"+"}").format("")
        for index, i in enumerate(self.columns):
            row += ('{:>'+f'{max_col[index] + 2}'+'}').format(i) 
        row += '\n'
        # rest rows
        for i in range(len(self.index)):
            a = self.index[i]
            row_values = self.values[i]
            row +=("{:>"+f"{max_index+2}"+"}").format(a)
            for index, b in enumerate(row_values):
                row += ('{:>'+f'{max_col[index] + 2}'+'}').format(b)
            row += '\n'
        result += row
        return result

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, col_list):
        col_mode = 1
        if isinstance(col_list, LabeledList):
            keys = col_list.values
        elif isinstance(col_list, list):
            if isinstance(col_list[0], str):
                keys = col_list
            elif isinstance(col_list[0], bool):
                col_mode = 0
        elif isinstance(col_list, str):
            keys = [col_list]
        
        if col_mode:
            zipped_values = list(zip(*self.values))
            
            col_index_list = []
            for key in keys:
                for col_index, col_name in enumerate(self.columns):
                    if key == col_name:
                        col_index_list.append( (col_index, key) )

            col_indexs, columns = zip(*col_index_list)
            select_data = []
            for index in col_indexs:
                row = zipped_values[index]
                select_data.append(row)

            if len(select_data) == 1:
                result = LabeledList(select_data[0], self.index)
            else:
                columns = list(columns)

                select_data = list(zip(*select_data))
                result = Table(select_data, self.index, columns)

            return result
        else:
            select_data = []
            select_index = []
            for index, isneed in enumerate(col_list):
                if isneed:
                    select_index.append(self.index[index])
                    select_data.append(self.values[index])
            return Table(select_data, select_index, self.columns)

    def head(self, n):
        row_select_list = [True] * n
        row_select_list += [False] * (len(self.index) - n)
        return self[ row_select_list ]

    def tail(self, n):
        row_select_list = [False] * (len(self.index) - n)
        row_select_list += [True] * n
        return self[ row_select_list ]

    def shape(self):
        return (len(self.values), len(self.values[0]))

def read_csv(fn):
    with open(fn, 'r') as file:
        csv_data = list(csv.reader(file))
        columns = csv_data[0]
        values = []
        for row in csv_data[1:]:
            if len(row) == 0:
                continue
            for i in range(len(row)):
                try:
                    row[i] = float(row[i])
                except ValueError:
                    pass
            values.append(row)

    return Table(values, columns=columns)






