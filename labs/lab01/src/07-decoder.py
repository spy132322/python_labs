#ЛАДНО НАПИШУ
#Но он не будет оптимальным
import re
inp = input()
fsymb: int
ssymb: int
d: int
for i in range(len(inp)):
    if re.match("([А-ЯA-Z])", inp[i]) != None:
        fsymb = i
        break

for i in range(len(inp)):
    if re.match("([0-9])", inp[i]) != None:
        ssymb = i + 1
        break
d =(ssymb-fsymb)
decoded: str = ""
for i in range(fsymb, len(inp), d):
    decoded = decoded + inp[i]
    if(inp[i] == "."):
        break
print(decoded)
