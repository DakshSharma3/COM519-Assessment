# def valid_check(text, function):
#     for character in text:
#         if function(character):
#             return True
#     return False
#
# string = "abcd123"
#
# print(valid_check(string,str.isdigit))
from com519.src.com519.database import Database

postcode = "so31 5gg"
address = "8 Cranmore"
db = Database("COM519.db")
# postcode = postcode.upper().replace(" ", "")
# query = """SELECT * FROM Address WHERE Postcode = ?;"""
# results = db.cursor.execute(query, (postcode,)).fetchall()
# print(results)

query = """INSERT INTO Address (Address, Postcode) VALUES (?, ?);"""
db.cursor.execute(query, (address, postcode))
db.connection.commit()
