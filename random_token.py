import random
import string

def random_token(N=12):
    token = ''.join(random.SystemRandom()
                .choice(string.ascii_uppercase + string.digits) for _ in range(N))
    return token