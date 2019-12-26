"""
Implement action to iteract with database
"""
import zerodb
import transaction
from models import Posts,Doctor
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
        # print(doctor)
        # try:
        #     doctors=self.db[Doctor].query(table_role="doctor")
        #     print(doctors)
        #     print('ggg')
        # except:
        #     LOG.error("Cannot get posts in database")

        with transaction.manager:
            try:
                print('kkkk')

                p = Doctor(email=doctor['email'],password=doctor['password'],table_role="doctor")
                print(p,'kkkk')
                self.db.add(p)
                transaction.commit()

                return True
            except:
                LOG.error("Cannot add Doctor")
        self.db.disconnect

    def _get_doctors(self,doctor=None):
        try:
            if doctor is None:
                doctor_record=self.db[Doctor].query(table_role="doctor")
                return list(doctor_record)
            else:
                doctor=self.db[Doctor].query(table_role="doctor",email=doctor['email'])
                return list(doctor)
        except:
            LOG.error("Cannot retrieve doctors")

    def _get_patients(self,patient=None):
        try:
            if patient is None:
                patient_record=self.db[Patient].query(table_role="patient")
                return list(doctor_record)
            else:
                doctor=self.db[Doctor].query(table_role="doctor",email=doctor['email'])
                return list(doctor)
        except:
            LOG.error("Cannot retrieve doctors")


    def _delete(self, post_id):
        try:
            post_record = self.db[Posts].query(pid=post_id)
            self.db.remove(post_record[0])
            transaction.commit()
            return True
        except:
            LOG.error("Cannot remove a post "
                      "with post ID: %s" % post['pid'])

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
