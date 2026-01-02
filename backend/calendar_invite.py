import random
import string

def schedule_interview():
    code = "".join(random.choices(string.ascii_lowercase, k=3))
    code2 = "".join(random.choices(string.ascii_lowercase, k=4))
    code3 = "".join(random.choices(string.ascii_lowercase, k=3))
    return f"https://meet.google.com/{code}-{code2}-{code3}"
