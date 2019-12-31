"""
Implement action to iteract with database
"""
import zerodb
import transaction
from models import Posts,Doctor,Appointment,Receptionist,Admin
import config
import log

import uuid
CONF = config.get_config()
LOG = log.setup_log("App")


class ZeroDBStorage(object):
    def __init__(self):
        """
        Init variables
        Read zerodb config from file
        """
        self.username = CONF.get('zerodb', 'username')
        self.password = CONF.get('zerodb', 'password')
        self.host = CONF.get('zerodb', 'host')
        self.port = int(CONF.get('zerodb', 'port'))
        print(self.username,self.password,self.host)
        self.db = zerodb.DB((self.host, self.port),
                            username=self.username,
                            password=self.password)
        self.db.enableAutoReindex()

    def _create(self, post):
        """
        Create a post
        """
        print(post)
        with transaction.manager:
            try:
                pid = str(uuid.uuid4())
                print(pid)
                p = Posts(pid=pid,
                          post_title=post['title'],
                          post_content=post['content'],
                          table_role="post")
                print(p)
                self.db.add(p)
                transaction.commit()

                return True
            except:
                LOG.error("Cannot create a post")
        self.db.disconnect


    def _create_doctor(self,doctor):
        """
        Create a post
        """
        with transaction.manager:
            try:
                print('kkkk')

                doctor_id = str(uuid.uuid4())
                p = Doctor(doctor_id=doctor_id,email=doctor['email'],password=doctor['password'],specialization=doctor['specialization'],name=doctor['name'],table_role="doctor")
                print(p,'kkkk')
                m=self.db.add(p)
                transaction.commit()
                return True
            except:
                LOG.error("Cannot add Doctor")
        self.db.disconnect







    def _create_appointment(self,appointment):
        """
        Create a post
        """
        with transaction.manager:
            try:
                print('kkkk')
                # p=db[Doctor].query(table_role="doctor",name=appointment['doctor_id'])

                appointment_id = str(uuid.uuid4())
                p = Appointment(appoint_id=appointment_id,
                    name=appointment['patient_name'],
                    blood_group=appointment['bloodgroup'],
                    recep_id=appointment['receptionist_id'],
                    date_time=appointment['datetime'],
                    age=appointment['age'],
                    doctor_id=appointment['doctor_id'],
                    table_role="appointment")

                print(p,'kkkk')
                self.db.add(p)
                transaction.commit()
                return True
            except:
                LOG.error("Cannot add Appointment")
        self.db.disconnect

    def _create_receptionist(self,reception):
        """
        Create a post
        """
        with transaction.manager:
            try:
                print('kkkk')
                # p=db[Doctor].query(table_role="doctor",name=appointment['doctor_id'])

                reception_id = str(uuid.uuid4())
                print(reception_id)
                p = Receptionist(recep_id=reception_id,
                    name=reception['name'],
                    password=reception['password'],
                    email=reception['email'],
                    table_role="receptionist")
                print(p)

                print(p,'kkkk')
                self.db.add(p)
                transaction.commit()
                return True
            except:
                LOG.error("Cannot add Receptionist")
        self.db.disconnect

    def _create_admin(self,admin):
        with transaction.manager:
            try:
                print('Hello')
                admin_id=str(uuid.uuid4())
                print(admin_id)
                print(admin['email'],admin['password'],admin['name'])
                p=Admin(admin_id=admin_id,name=admin['name'],email=admin['email'],password=admin['password'],table_role="admin")
                print(p)
                self.db.add(p)
                transaction.commit()

                return True

            except:
                LOG.error('Cannot Register Admin')



    def _authenticate_admin(self,cred):
        try:
            print('Hello')
            email=str(cred['email'])
            print(email)
            admin=self.db[Admin].query(table_role="admin",email=email)
            print(admin)
            if admin[0].email == cred['email']:
                if admin[0].password == cred['password']:
                    return True
                else:
                    return False
            else:
                return False



        except:
            print('Proeblem accord')



    def _authenticate_doctor(self,cred):
        try:
            print(cred)
            email=str(cred['email'])
            print(email)
            doctor=self.db[Doctor].query(table_role="doctor",email=email)
            print(doctor)
            print(doctor[0].password)
            print(cred['password'])
            # password1=doctor[0].password
            # password2=cred.password
            # print(password1,password2)

            if str(doctor[0].password) == str(cred['password']) :
                return True

            # if doctor[0] is not None:
            #     print(doctor[0],password)
            #     check=doctor[0]
            #     if doctor[0].password == cred.password :
            #         return True
            #     else:
            #         return False
            else:
                return False

        except:
            LOG.error("Cannot Authenticate Doctor")

    def _authenticate_receptionist(self,cred):
        try:
            print(cred)
            email=str(cred['email'])
            print(email)
            receptionist=self.db[Receptionist].query(table_role="receptionist",email=email)
            print(receptionist)
            print(receptionist[0].password)
            print(cred['password'])


            if str(receptionist[0].password) == str(cred['password']) :
                return True,receptionist[0]

            # if doctor[0] is not None:
            #     print(doctor[0],password)
            #     check=doctor[0]
            #     if doctor[0].password == cred.password :
            #         return True
            #     else:
            #         return False
            else:
                return False

        except:
            LOG.error("Cannot Authenticate Receptionist")


    def _get_doctors(self,doctor=None):
        try:
            if doctor is None:
                
                s=self.db[Doctor].query(table_role="doctor")
                
                print(s[0].doctor_id)
                doctor_record=self.db[Doctor].query(table_role="doctor")
                return list(doctor_record)
            else:
                doctor=self.db[Doctor].query(table_role="doctor",email=doctor['email'])
                return list(doctor)
        except:
            LOG.error("Cannot retrieve doctors")

    def _get_appointments(self,patient=None):
        try:
            if patient is None:
                patient_record=self.db[Appointment].query(table_role="appointment")
                return list(patient_record)
            else:
                patient=self.db[Appointment].query(table_role="appointment",email=patient['name'])
                return list(patient)
        except:
            LOG.error("Cannot retrieve doctors")

    def _get_receptionist(self,receptionist=None):
        try:
            if receptionist is None:
                recep=self.db[Receptionist].query(table_role="receptionist")
                return list(recep)
            else:
                receptionist=self.db[Receptionist].query(table_role="receptionist",id=receptionist['id'])
                return list(receptionist)
        except:
            LOG.error("Cannot Retrive Receptionists")

    def _delete(self, pid):
        try:
            post_record = self.db[Posts].query(pid=pid)
            self.db.remove(post_record[0])
            transaction.commit()
            return True
        except:
            LOG.error("Cannot remove a post "
                      "with post ID: %s" % post['pid'])


    def _delete_p(self, email):
        try:
            post_record = self.db[Doctor].query(table_role="doctor",email=email)
            print(post_record)
            self.db.remove(post_record[0])
            transaction.commit()
            return True
        except:
            LOG.error("Cannot remove a Doctor")
    
    def _delete_r(self, email):
        try:
            post_record = self.db[Receptionist].query(table_role="receptionist",email=email)
            print(post_record)
            self.db.remove(post_record[0])
            transaction.commit()
            return True
        except:
            LOG.error("Cannot remove a Receptionist")

    def _delete_doctor(self,doctor_id):
        try:
            print('dssss')
            print('aaa',docter_id)
            print('dssss')

            if doctor_id is not None:

                doctor=self.db[Doctor].query(table_role="doctor")
                print(doctor[0])
                return True
            else:
                return False
            # self.db.remove(post_record[0])
            # transaction.commit()
            
        except:
            LOG.error('Cannot remove Doctor')

    def _delete_receptionist(self, reception_id):
        try:
            post_record = self.db[Receptionist].query(recep_id=reception_id)
            self.db.remove(post_record[0])
            transaction.commit()
            return True
        except:
            LOG.error("Cannot remove a post "
                      "with post ID: %s" % post['doctor_id'])

    def _get(self, pid=None):
        try:
            if pid is None:
                posts = self.db[Posts].query(table_role="post")
                print(posts)
                LOG.debug("Posts: " + str(list(posts)))
                return list(posts)
            else:
                post = self.db[Posts].query(table_role="post",
                                            pid=pid)
                LOG.debug("Post: " + str(list(post)))
                return list(post)
        except Exception as e:
            LOG.error("Cannot get posts in database: %s" % e)
