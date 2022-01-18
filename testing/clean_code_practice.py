# class User:
#     def __init__(self, first_name: str, age: int):
#         self.first_name = first_name
#         self.age = age

#     def save(self):
#         print("saving!")

#     def isValid(self) -> bool:
#         print("validating user")
#         valid_name = False
#         valid_age = False
#         if len(self.first_name) > 0:
#             valid_name = True
#         if self.age > 0 and self.age < 150:
#             valid_age = True
#         return (valid_name and valid_age)


# user = User("taco", 160)

# print(user.isValid())
from dataclasses import dataclass, field

@dataclass(order=True)
class Database():
    sort_index: int = field(init=False)
    host: str
    port: str
    priority: int = 5
        
    def url(self):
        return f'{self.host}/{self.port}'
    
    def __post_init__(self):
        self.sort_index = self.priority
        
    def __str__(self) -> str:
        return f'{self.host}-{self.priority}/{self.port}'
    
db_1 = Database('mytaco', '3000', 1)
db_2 = Database('mytaco2', '3000', 2)
db_3 = Database('mytaco3', '3000', 6)

print(db_1.priority)
print(db_1>db_2)
