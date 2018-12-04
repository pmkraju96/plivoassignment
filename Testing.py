import unittest
import requests


class Testing(unittest.TestCase):

    def test_auth_success(self):
        key = "1086dc1c-f793-11e8-8450-28e347a032ef"
        url = "http://localhost:5000/?key="+key
        res = requests.get(url = url)
        b = "Welcome to the Contact Book Api admin@gmail.com"
        self.assertEqual(res.text, b)

    def test_auth_failure(self):
        key = "randomkey"
        url = "http://localhost:5000/?key="+key
        res = requests.get(url = url)
        b = "invalid key access denied"
        self.assertEqual(res.text, b)

    def test_auth_no_key(self):
        key = ""
        url = "http://localhost:5000/?key="+key
        res = requests.get(url = url)
        b = "please provide access key for api"
        self.assertEqual(res.text, b)


    def test_add_contact(self):
    	key = "1086dc1c-f793-11e8-8450-28e347a032ef"
    	url = "http://localhost:5000/addContact?key="+key+"&name=vani&email=vani@gmail.com&number=9852312215"
    	res = requests.get(url=url)
    	b = "Contact Added Successfully"
    	self.assertEqual(res.text,b)


    def test_add_contact_without_key(self):
    	key = "1086dc1c-f793-11e8-8450-28e347a032ef"
    	url = "http://localhost:5000/addContact?name=vani&email=vani@gmail.com&number=9852312215"
    	res = requests.get(url=url)
    	b = "invalid key access denied"
    	self.assertEqual(res.text, b)


if __name__ == '__main__':
    unittest.main()