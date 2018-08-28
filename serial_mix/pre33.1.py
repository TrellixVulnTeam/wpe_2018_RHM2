# Notes from Tad
"""
This exercise #33 is about using mixins, but after completing my solution
I was starting to wonder whether it would work in a more general case.
When the data attributes of the Book class are all primitive (strings or numbers)
there is no problem, except serializing to CSV. When loading back from file everything
is converted to strings, so the price attribute becomes string, while the original one was float.
Perhaps some additional step, converting to numbers everything what looks like a number,
would fix this. In the case of XML generated by dicttoxml the data type is written to the file,
so the full restoration of original data is possible using eval (as I did, but most likely this
is a security hole). Now, what about more complicated cases? To test this I added to the Book
class some additional attributes. Lists and dictionaries were restored OK from pickle and JSON files,
from CSV everything was a string, of course. XML was written fine, it seems, but restoring has failed.
The reason is clear – my solution decodes only top-level tags, but with list and dictionaries there
are nested tags in the file. I am sure, it is possible to solve this using some recursive procedures,
so the full restoration of data attributes from XML file should be possible. Next I have added as an
attribute an instance of a custom class, with its own attributes. In this case only pickling and
unpickling worked fine, fully restoring the data. Sure, it’s not surprising as this is a native Python
serialization. XML and JSON were not able to serialize at all. In conclusion, serialization is not a
trivial task when we want to use some portable format and for more complicated data it requires writing
specialised custom functions.
"""


import pickle
import csv
import json
import dicttoxml, xmltodict


class Serializable:

    def dump(self, filename):
        self._write_attributes(filename)

    def load(self, filename):
        obj = self._read_attributes(filename)
        self.__dict__.clear()
        self.__dict__.update(obj)

    def _write_attributes(self, filename):
        with open(filename, 'wb') as pickle_file:
            pickle.dump(self.__dict__, pickle_file, pickle.HIGHEST_PROTOCOL)

    def _read_attributes(self, filename):
        with open(filename, 'rb') as pickle_file:
            data = pickle.load(pickle_file)
        return data


class CSVMixin:

    def _write_attributes(self, filename):
        with open(filename, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, self.__dict__.keys())
            writer.writeheader()
            writer.writerow(self.__dict__)

    def _read_attributes(self, filename):
        with open(filename, 'r') as csv_file:
            data = next(csv.DictReader(csv_file))
        return data


class JSONMixin:

    def _write_attributes(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.__dict__, json_file)

    def _read_attributes(self, filename):
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data


class XMLMixin:

    def _write_attributes(self, filename):
        xml = dicttoxml.dicttoxml(self.__dict__)
        with open(filename, 'w') as xml_file:
            xml_file.write(xml.decode())

    def _read_attributes(self, filename):
        with open(filename, 'r') as xml_file:
            obj = xmltodict.parse(xml_file.read())
        data = {key: eval(obj['root'][key]['@type'])(obj['root'][key]['#text'])
                for key in obj['root'].keys()}
        return data


# -- TESTS ---

# Pickle test
class Book1(Serializable):

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def __str__(self):
        return str(self.__dict__)


print('\nPickle test')
b1 = Book1('Example title - pickle', 'Example author', 25.75)
print(b1)
b1.dump('w33.pickle')
b2 = Book1('a', 'b', 0)
print(b2)
b2.load('w33.pickle')
print(b2)


# CSV test
class Book2(CSVMixin, Serializable):

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def __str__(self):
        return str(self.__dict__)


print('\nCSV Test')
b1 = Book2('Example title - CVS', 'Example author', 25.75)
print(b1)
b1.dump('w33.csv')
b2 = Book2('c', 'd', 0)
print(b2)
b2.load('w33.csv')
print(b2)


# JSON test
class Book3(JSONMixin, Serializable):

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def __str__(self):
        return str(self.__dict__)


print('\nJSON test')
b1 = Book3('Example title - JSON', 'Example author', 25.75)
print(b1)
b1.dump('w33.json')
b2 = Book3('e', 'f', 0)
print(b2)
b2.load('w33.json')
print(b2)


# XML Test
class Book4(XMLMixin, Serializable):

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def __str__(self):
        return str(self.__dict__)


print('\nXML test')
b1 = Book4('Example title - XML', 'Example author', 25.75)
print(b1)
b1.dump('w33.xml')
b2 = Book4('g', 'h', 0)
print(b2)
b2.load('w33.xml')
print(b2)
