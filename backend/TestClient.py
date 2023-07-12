from requests import Session

s = Session()


r = s.post("http://localhost:8000/items/create/user", json={"email":"deanmostafa7@gmail.com", "password":"ABCD"})
print(r.status_code)
print(r.text)




