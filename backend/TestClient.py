from requests import Session

s = Session()

r = s.post("http://localhost:8000/authenticate", json={"email":"jaysmith.budhut@gmail.com", "password":"ABCD"})
print(r.status_code)
print(r.text)

r = s.post("http://localhost:8000/items/update/metadata?id=a3b546f7-533e-4a2a-af1d-d3471dfd70b9", json={"name":"NewJay453", "path":[]})
print(r.status_code)
print(r.text)


