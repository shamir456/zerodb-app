import names
import loremipsum
import random

from database import ZeroDBStorage
Temp_patients = [
{
  "name":"Fahad",
  "Date":"16-1-19",
  "Time":"7 pm",
  "Age":"20",
  "BldGrp":"A+",
},
{
  "name":"Shameer",
  "Date":"16-1-20",
  "Time":"2 pm",
  "Age":"10",
  "BldGrp":"B+",
},
{
  "name":"Mujtaba Bawani",
  "Date":"13-1-19",
  "Time":"6 pm",
  "Age":"50",
  "BldGrp":"B+",
},
]
Temp_doctors = [
{
  "name":"Ammar Rizwan",
  "email":"test@gmail.com",
  "specialization":"MBBS",
  "password":"Hello"
},
{
  "name":"Moazzam Maqsood",
  "email":"test@gmail.com",
  "specialization":"MBBS",
   "password":"Hello1"

},
{
  "name":"Faizan Saleem",
  "email":"test@gmail.com",
  "specialization":"MBBS",
  "password":"Hello2"

},
]

Temp_receptionist = [
{
  "name":"Faizan",
  "email":"test1@gmail.com",
  "password":"Hello2"

},
{
  "name":"Abdul Hameed",
  "email":"test2@gmail.com",
   "password":"Hello3"

},
{
  "name":"Tahir Hemani",
  "email":"test3@gmail.com",
  "password":"Hello3"

},
]


try:
   admin={"name":"Fahad","email":"hello@gmail.com","password":"Hello2"}
   zero = ZeroDBStorage()
   m='test3@gmail.com'
   post_id='ef9e292b-a219-448a-8891-0ba7d786f3c6'
   # print(zero._get_doctors())
   # print(zero._get())
   print(zero._delete_r(email=m))
  # print(zero._delete_doctor())

   # if(zero._create_admin(admin=admin)):
   #  print('Created')
   # else:
   #  print('Not working')

except Exception as e:
	print("Could not happen")
