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
	# for doctor in Temp_doctors:

	# 	zero = ZeroDBStorage()

	# 	print(zero._create_doctor(doctor))

	for receptionist in Temp_receptionist:
		zero = ZeroDBStorage()
		print(zero._create_receptionist(receptionist))

except Exception as e:
	print("Could not happen")
