#https://github.com/serengil/LightPHE
from lightphe import LightPHE
import pickle
import base64

#Testing cryptosystem
cs = LightPHE(algorithm_name = "Exponential-ElGamal") # additively homomorphic

x = 17
y = 19

c1 = cs.encrypt(x)
c2 = cs.encrypt(y)

'''
print(type(c1))
print(type(c1.value))  
print(c1.value)
'''

serialized_ciphertext = pickle.dumps(c1)

serialized_ciphertext_base64 = base64.b64encode(serialized_ciphertext).decode('utf-8')

print(serialized_ciphertext_base64)


#obj = pickle.loads(serialized_ciphertext)