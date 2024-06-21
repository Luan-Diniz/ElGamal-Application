#https://github.com/serengil/LightPHE
from lightphe import LightPHE

#Testing cryptosystem
cs = LightPHE(algorithm_name = "Exponential-ElGamal") # additively homomorphic

x = 17
y = 19

c1 = cs.encrypt(x)
c2 = cs.encrypt(y)

# __add__ is defined in the library
# It is defined the operator "+" for the class Ciphertexts
print(type(c1))  

c3 = c1 + c2   
result = cs.decrypt(c3)
print(f"Result: {result}, should be {x + y}")


cs2 = LightPHE(algorithm_name = "ElGamal") # multiplicatively homomorphic
c1 = cs2.encrypt(x)
c2 = cs2.encrypt(y)
c3 = c1 * c2
result = cs2.decrypt(c3)
print(f"Result: {result}, should be {x * y}")


cs.export_keys("public_key.key", True)
cs_publickey = LightPHE(algorithm_name = "Exponential-ElGamal", key_file= "public_key.key")

d1 = cs_publickey.encrypt(10)
d2 = cs_publickey.encrypt(10)

assert ((d1==d2) == False)  # d1 and d2 must be diferent.



