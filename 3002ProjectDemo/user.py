import json

class User(object):
    def __init__(self):
        self.user_info = json.load(open("database.txt"))
    
    def fetch_info(self, field):
        return json.load(open("database.txt")).get(field, 'key word error')
    
    def edit_info(self, field, data):
        self.user_info = json.load(open("database.txt"))
        self.user_info[field] = data
        json.dump(self.user_info, open("database.txt",'w'))
        
if __name__ == "__main__":
    Demo = User()
    # Demo.edit_info('username', 'XU')
    # print(Demo.user_info)
    # print(Demo.fetch_info('password'))
    # Demo.edit_info('account', '12234')
    # print(Demo.user_info)
    print(Demo.fetch_info('option'))

