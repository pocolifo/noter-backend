from requests import Session

s = Session()

r = s.post("http://localhost:8000/authenticate", json={"email":"myemail2@gmail.com", "password":"ABCD"})
print(r.status_code)
print(r.text)

r = s.get("http://localhost:8000/items/f4a0c620-dc41-418a-aac9-6bf7b1e5b5ee")
print(r.status_code)
print(r.text)


