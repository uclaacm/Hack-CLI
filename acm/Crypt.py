from datetime import datetime as OO0O0O00O0O00O00O 
G =int 
j =round 
W =ord 
t =range 
h =str 
F =zip 
v =list 
S =len 
K =OO0O0O00O0O00O00O .utcnow 
import os as OO0000000000O0O00 ,hashlib as O0O00O00OO0O0O000 
g =OO0000000000O0O00 .urandom 
l =O0O00O00OO0O0O000 .sha256 
i ="a076ef2e85154871eb365ecb4942bfd5"
def U ():
	return G (j ((K ()-OO0O0O00O0O00O00O (1970 ,1 ,1 )).total_seconds ()*1000 ))
def Y (OOO00O00O0O0O0OO0 ):
	O00OO00OOOOO00000 =lambda :"0123456789abcdef"[W (g (1 ))%16 ]
	return "".join (O00OO00OOOOO00000 ()for OOO0O00000OOOOOOO in t (OOO00O00O0O0O0OO0 ))
def u ():
	OOO0OO0OOO0OO00OO =h (U ())
	O0OOOO0OO00OO0O00 ="".join ([O0O0O00OO000OO00O +OOO00000O0000O000 for (O0O0O00OO000OO00O ,OOO00000O0000O000 )in F (v (OOO0OO0OOO0OO00OO ),v (Y (S (OOO0OO0OOO0OO00OO ))))])
	return  O0OOOO0OO00OO0O00 +l (OOO0OO0OOO0OO00OO +i ).hexdigest ()
def getToken ():return u ()

