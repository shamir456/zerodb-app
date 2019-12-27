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





class Appointment(Model):

    appoint_id=Field()
    name=Field()
    age=Field()
    blood_group=Field()
    date_time=Field()
    doctor_id=Field()
    recep_id=Field()
    table_role=Field()

    def __repr__(self):
        return str({
            "name":self.name,
            "doctor_id":self.doctor_id,
            "age":self.age,
            "recep_id":self.recep_id,
            "date_time":self.date_time,
            "blood_group":self.blood_group,
            "table_role":self.table_role
            })


class Receptionist(Model):
    recep_id=Field()
    name=Field()
    password=Field()
    email=Field()
    table_role=Field()

    def __repr__(self):
        return str({
            "recep_id":self.recep_id,
            "name":self.name,
            "password":self.password,
            "email":self.email,
            "table_role":self.table_role

            })



class Admin(Model):

    admin_id=Field()
    name=Field()
    password=Field()
    email=Field()
    table_role=Field()

    def __repr__(self):
        return str({
            "admin_id":self.admin_id,
            "name":self.name,
            "password":self.password,
            "email":self.email,
            "table_role":self.table_role

            })





    
