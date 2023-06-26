import psycopg2, json
from datetime import datetime
from starlette.requests import Request

class DB:
    def __init__(self, dbname, user, password, host, port):
        self.conn = None
        self.cur = None
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self): # Returns True if connection to database is successful
        try:
            self.conn = psycopg2.connect(database=self.dbname, user=self.user, password=self.password, 
                                                            host=self.host, port=self.port)
            self.cur = self.conn.cursor()
            return True
        except:
            return False

        
    def is_authenticated(self, request: Request) -> bool:
        self.cur.execute("SELECT * FROM users WHERE users.info->>'id' = '{0}'".format(str(request.cookies.get("authenticate"))))
        rows = self.cur.fetchall()
        if len(rows) != 0:
            return True
        return False
    
    
    def does_path_exist(self, request: Request, fullpath: list):
        if len(fullpath) == 0: return True
        self.cur.execute("SELECT * FROM folders WHERE folders.info->'metadata'->'owner'->>'id' = '{0}'".format(str(request.cookies.get("authenticate"))))
        rows = self.cur.fetchall()
        for r in rows:
            if str(r[0]["metadata"]["name"]) == str(fullpath[-1]):
                if str(r[0]["metadata"]["path"]) == str(fullpath[:-1]): # Remove last element and compare rest of path
                    return True
        return False

    def get_item(self, request: Request, id: str):
        self.cur.execute("""SELECT * from notes WHERE notes.info->>'id' = '{0}' 
        AND notes.info->'metadata'->'owner'->>'id' = '{1}'
        """.format(id, request.cookies.get("authenticate")))
        try: return json.dumps(self.cur.fetchall()[0][0])
        except:
            self.cur.execute("""SELECT * from folders WHERE folders.info->>'id' = '{0}' 
            AND folders.info->'metadata'->'owner'->>'id' = '{1}'
            """.format(id, request.cookies.get("authenticate")))
            try: return json.dumps(self.cur.fetchall()[0][0])
            except: return False
        

    def get_user_data_by_id(self, id: str):
        self.cur.execute("SELECT * FROM users WHERE users.info->>'id' = '{0}'".format(id))
        try: return json.dumps(self.cur.fetchall()[0][0])
        except: return False

    def insert_note(self, note: str):
        self.cur.execute("INSERT INTO notes (INFO) VALUES('{0}')".format(json.dumps(json.loads(note)))) # Load then dump to make sure JSON isn't multi-lined
        self.conn.commit()
    
    def insert_folder(self, folder: str):
        self.cur.execute("INSERT INTO folders (INFO) VALUES('{0}')".format(json.dumps(json.loads(folder)))) # Load then dump to make sure JSON isn't multi-lined
        self.conn.commit()

    def delete_item_by_id(self, request: Request, id: str):
        self.cur.execute("""DELETE FROM folders 
        WHERE folders.info->>'id' = '{0}' 
        AND folders.info->'metadata'->'owner'->>'id' = '{1}'""".format(id, request.cookies.get("authenticate")))
        
        self.cur.execute("""DELETE FROM notes 
        WHERE notes.info->>'id' = '{0}' 
        AND notes.info->'metadata'->'owner'->>'id' = '{1}'""".format(id, request.cookies.get("authenticate")))
        self.conn.commit()

    def update_metadata_by_id(self, request: Request, id: str, new_name: str, new_path: str): 
        new_name = json.dumps(new_name)
        self.cur.execute("""UPDATE notes SET info = jsonb_set(info::jsonb, '{metadata,name}', %s::jsonb)
        WHERE info->>'id' = %s 
        AND info->'metadata'->'owner'->>'id' = %s""", (new_name, id, request.cookies.get("authenticate"))) # Not using .format method because of update path
        
        self.cur.execute("""UPDATE notes SET info = jsonb_set(info::jsonb, '{metadata,path}', %s::jsonb)
        WHERE info->>'id' = %s 
        AND info->'metadata'->'owner'->>'id' = %s""", (new_path, id, request.cookies.get("authenticate")))
        
        self.cur.execute("""UPDATE notes SET info = jsonb_set(info::jsonb, '{metadata,lastEdited}', %s::jsonb)
        WHERE info->>'id' = %s 
        AND info->'metadata'->'owner'->>'id' = %s""", (json.dumps(str(datetime.now().isoformat())), id, request.cookies.get("authenticate")))
        
        self.cur.execute("""UPDATE folders SET info = jsonb_set(info::jsonb, '{metadata,name}', %s::jsonb)
        WHERE info->>'id' = %s 
        AND info->'metadata'->'owner'->>'id' = %s""", (new_name, id, request.cookies.get("authenticate")))
        
        self.cur.execute("""UPDATE folders SET info = jsonb_set(info::jsonb, '{metadata,path}', %s::jsonb)
        WHERE info->>'id' = %s 
        AND info->'metadata'->'owner'->>'id' = %s""", (new_path, id, request.cookies.get("authenticate")))
        
        self.cur.execute("""UPDATE folders SET info = jsonb_set(info::jsonb, '{metadata,lastEdited}', %s::jsonb)
        WHERE info->>'id' = %s 
        AND info->'metadata'->'owner'->>'id' = %s""", (json.dumps(str(datetime.now().isoformat())), id, request.cookies.get("authenticate")))
        
        self.conn.commit()
        
    def update_blocks_by_id(self, request: Request, id: str, new_blocks: str):
        self.cur.execute("""UPDATE notes SET info = jsonb_set(info::jsonb, '{blocks}', %s::jsonb) 
        WHERE info->>'id' = %s 
        AND info->'metadata'->'owner'->>'id' = %s""", (new_blocks, id, request.cookies.get("authenticate")))
        
        self.cur.execute("""UPDATE notes SET info = jsonb_set(info::jsonb, '{metadata,lastEdited}', %s::jsonb) 
        WHERE info->>'id' = %s 
        AND info->'metadata'->'owner'->>'id' = %s""", (json.dumps(str(datetime.now().isoformat())), id, request.cookies.get("authenticate")))
        
        self.conn.commit()

    def update_lastsignedin(self, request: Request):
        self.cur.execute("""UPDATE users SET info = jsonb_set(info::jsonb, '{lastSignedIn}', %s::jsonb) 
        WHERE info->>'id' = %s""", (json.dumps(str(datetime.now().isoformat())), request.cookies.get("authenticate")))
        self.conn.commit()

    def get_users_notes(self, request: Request):
        ret = []
        self.cur.execute("SELECT * FROM notes WHERE notes.info->'metadata'->'owner'->>'id' = '{0}'".format(str(request.cookies.get("authenticate"))))
        rows = self.cur.fetchall()
        for r in rows:
            ret.append(r[0])
        return ret
    
    def get_users_by_email(self, email: str):
        ret = []
        self.cur.execute("SELECT * from users WHERE users.info->>'email' = '{0}'".format(email))
        rows = self.cur.fetchall()
        for r in rows:
            ret.append(r[0])
        return ret
        
        
    
