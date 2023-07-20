from requests import Session

s = Session()


r = s.post("http://localhost:8000/authenticate", json={"email":"jaysmith.budhut@gmail.com", "password":"ABCD"})
print(r.status_code)
print(r.text)

r = s.post("http://localhost:8000/items/update/name", json={"name":"xxx_Jay_xxx"})
print(r.status_code)
print(r.text)

r = s.post("http://localhost:8000/items/update/pfp", json={"image":"newPFP"})
print(r.status_code)
print(r.text)

"""
r = s.put("http://localhost:8000/items/update/blocks?id=aa38c54c-c44d-4f68-97ad-5756b61e2582", json=["234728"])
print(r.status_code)
print(r.text)
"""