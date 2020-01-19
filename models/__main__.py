from .repo import Repo
from .User import User

r = Repo()

u = User("dimas", 123, 321, "aaa")


r.create_any(u)
