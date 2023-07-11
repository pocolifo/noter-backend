from requests import Session

s = Session()

r = s.post("http://localhost:8000/authenticate", json={"email":"myemail2@gmail.com", "password":"ABCD"})
print(r.status_code)
print(r.text)

r = s.post("http://localhost:8000/items/list", json=[])
print(r.status_code)
print(r.text)



