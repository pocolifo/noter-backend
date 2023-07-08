from requests import Session

s = Session()


r = s.post("http://localhost:8000/authenticate", json={"email":"myemail2@gmail.com", "password":"ABCD"})
print(r.status_code)
#print(r.text)


r = s.put("http://localhost:8000/items/update/blocks?id=9e73f768-6fca-4494-a6b6-9287754a3734", json=[     {         "type": "text",         "data": {             "content": "<serialized data>"         }     },     {         "type": "image",         "data": {             "url": "<serialized URL data>"         }     } ])
print(r.status_code)
print(r.text)


r = s.get("http://localhost:8000/")
print(r.status_code)
#print(r.text)





