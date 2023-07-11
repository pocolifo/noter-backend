from requests import Session

s = Session()


r = s.post("http://localhost:8000/items/create/user", json={"email":"john3@gmail.com", "password":"BBCD"})
print(r.status_code)
print(r.text)

r = s.post("http://localhost:8000/items/create/note", json={"name":"autoauth", "path":[]})
print(r.status_code)
print(r.text)



