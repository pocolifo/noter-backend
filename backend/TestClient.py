from requests import Session

s = Session()


r = s.post("http://localhost:8000/authenticate", json={"email":"john@gmail.com", "password":"ABCD"})
print(r.status_code)
print(r.text)

r = s.post("http://localhost:8000/verify?id=5dcb4269-d48b-4132-a03d-1c7d2840a012")
print(r.status_code)
print(r.text)



