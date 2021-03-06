import os
import unittest
from snow_connector_pck.snow_connector import MakeSnowConnection
from dotenv import load_dotenv

class BasicTestCase(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.base_url = os.getenv('BASE_URL')
        self.snow_usr = os.getenv('SNOW_USR')
        self.snow_pwd = os.getenv('SNOW_PWD')
        self.connection = MakeSnowConnection(self.base_url, self.snow_usr, self.snow_pwd)

    def test_get_variable_url(self):
        """test if environment variables are being retrieved - url"""
        self.base_url = os.getenv('BASE_URL')
        self.assertTrue(self.base_url != None)
    
    def test_get_variable_user(self):
        """test if environment variables are being retrieved - user"""
        self.base_url = os.getenv('SNOW_USR')
        self.assertTrue(self.base_url != None)

    def test_get_variable_password(self):
        """test if environment variables are being retrieved - password"""
        self.base_url = os.getenv('SNOW_PWD')
        self.assertTrue(self.base_url != None)

    def test_get_single_inc_OK(self):
        """test if existing incident can be found"""
        response = self.connection.get_single_incident("INC0010111")
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertNotEqual(response['result'], [])
        self.assertIn('INC0010111',response['result'][0]['number'])

    def test_get_single_inc_ERR(self):
        """test if non existing object is not found"""
        response = self.connection.get_single_incident("Banan")
        response = response.json()
        self.assertEqual(response['result'], [])
        
    def test_get_multiple_incidents(self):
        """test fetching multiple incidents"""
        response_one = self.connection.get_multiple_incident()
        response_two = self.connection.get_multiple_incident(2)
        self.assertEqual(response_one.status_code, 200)
        self.assertEqual(response_two.status_code, 200)
        response_one = response_one.json()
        response_two = response_two.json()
        self.assertTrue(len(response_one['result']) != 0)
        self.assertTrue(len(response_two['result']) == 2)

    def test_get_single_email(self):
        """ test fetching single email object """ 
        sys_id = ''
        response = self.connection.get_single_email()
        response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sys_id, response['result'][0]['sys_id'])
        

    def test_get_single_user(self):
        """ test fetching single user """ 
        sys_id = ''
        response = self.connection.get_single_user()
        response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sys_id, response['result'][0]['sys_id'])
        self.assertEqual('Test', response['result'][0]['name'])
        

