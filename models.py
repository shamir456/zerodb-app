from zerodb.models import Model, Field, Text


class Posts(Model):
    """
    Model for Posts table
    """
    pid = Field()
    post_title = Field()
    post_content = Text()
    table_role = Field()

    def __repr__(self):
        return str({"pid": self.pid,
                    "post_title": self.post_title,
                    "post_content": self.post_content,
                    "table_role": self.table_role})

class Doctor(Model):
    """
    Model for Doctor table
    """
    doctor_id = Field()
    email = Field()
    password = Field()
    specialization=Field()
    name=Field()
    table_role = Field()

    def __repr__(self):
        return str({"doctor_id":self.doctor_id,
                    "email": self.email,
                    "password": self.password,
                    "specialization":self.specialization,
                    "name":self.name,
                    "table_role": self.table_role})

class Patient(Model):
    patient_id = Field()
    name=Field()
    age=Field()
    blood_group=Field()
    table_role=Field()

    def __repr__(self):
        return str({
            "patient_id":self.patient_id,
            "name":self.name,
            "age":self.age,
            "blood_group":self.blood_group,
            "table_role":self.table_role
            })




class Appointment(Model):

    pid=Field()
    count=Field()
    date_time=Field()
    doctor_id=Field()
    recep_id=Field()
    table_role=Field()



class Receptionist(Model):
    pid=Field()
    name=Field()
    
