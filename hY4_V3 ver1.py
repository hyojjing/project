import os
import sys
import time
from io import BytesIO
import tkinter
from tkinter import filedialog
import getpass
import zlib # zlib 디컴프레스 위한
import olefile # OLE 파서 이용
from threading import Thread
import psutil

def divide_list(l, n): 
   for i in range(0, len(l), n): 
      yield l[i:i + n]

def hex_check(path,filename):
   checklist = [0 for _ in range(11)]
   hexlist = [0 for _ in range(256)]
   ole = olefile.OleFileIO(path+'/'+filename)
   olename = ole.listdir()
   uname = getpass.getuser()
   size = []

   for x in range(len(olename)):
      zerolist = [0 for _ in range(256)]

      if len(olename[x]) == 2:
         if olename[x][0] != "DocOptions":
            stream = ole.openstream(olename[x][0]+'/'+olename[x][1])
            stream = BytesIO(zlib.decompress(stream.read(), -15))
            rest = stream.getvalue().hex()
            n = 2
            result = list(divide_list(rest, n))

            for k in range(len(result)):
               zerolist[int(result[k],16)] += 1
               hexlist[int(result[k],16)] += 1

            size.append(sum(zerolist)-zerolist[0])

            if "BinData" in olename[x][0]:   # ps 또는 eps 라는 확장자를 가진 스트림이 있는지
               if ".PS" or ".eps" in olename[x][1]: 
                  checklist[0] = 1
                  for y in range(len(result)):
                     if result[y] == '53' and result[y+1] == '74' and result[y+2]=='61' and result[y+3] == '72' and result[y+4]=='74' and result[y+5] == '75' and result[y+6]=='70':
                        checklist[1] = 1

                     if result[y] == '4d'  and result[y+1] == '5a':
                        checklist[2] = 1

                     if (result[y] == '72'  and result[y+1] == '65' a`nd result[y+2] == '61'  and result[y+3] == '64') or (result[y] == '77' and result[y+1] == '72' and result[y+2]=='69' and result[y+3] == '74' and result[y+4]=='65' ):
                        checklist[3] = 1
                           
                     if (result[y] == '2f' and result[y+1] == '65' and result[y+2]=='6e' and result[y+3] == '76' and result[y+4]=='73' and result[y+5] == '74' and result[y+6] == '72') or (result[y] == '2f' and result[y+1] == '61' and result[y+2]=='70' and result[y+3] == '70' and result[y+4]=='65' and result[y+5] == '6e' and result[y+6] == '76') or (result[y] == '2f' and result[y+1] == '66' and result[y+2]=='69' and result[y+3] == '6c' and result[y+4]=='65' ) or (result[y] == '2f' and result[y+1] == '70' and result[y+2]=='61' and result[y+3] == '74' and result[y+4]=='68' ):
                        checklist[4] = 1

                     if result[y] == '78' and result[y+1] == '6f' and result[y+2]=='72':
                        checklist[5] = 1

                     if result[y] == '63' and result[y+1] == '76' and result[y+2]=='78' and result[y+3] == '20' and result[y+4] == '65' and result[y+5] == '78' and result[y+6]=='65' and result[y+7]=='63':
                        checklist[6] = 1

                     if result[y] == '90' and result[y+1] == '90' and result[y+2] == '90':
                        checklist[7] = 1
         for y in range(len(result)):
            if (result[y] == '70' and result[y+2] == '6f' and result[y+4]=='77' and result[y+6] == '65' and result[y+8] == '72' and result[y+10] == '73' and result[y+12] == '68' and result[y+14] == '65' and result[y+16] == '6c' and result[y+18] == '6c'):
               checklist[10] = 1

   avg = 0
   
   for x in range(len(hexlist)):
      avg += hexlist[x]
   avg = avg -hexlist[0]
   avg = avg / len(hexlist)

   mycheck = []

   for i in range(len(hexlist)):
      if hexlist[i] > avg:
         mycheck.append(hexlist[i])

   print(mycheck)
   if len(mycheck) == 1:
      checklist[8] = 1

   mycheck.sort(reverse=True)
   if len(mycheck) >=2:
      if mycheck[0] > 2 * int(mycheck[1]):
         checklist[8] = 1

   
   
   biteavg = 0 
   for x in range(len(size)):
      biteavg += size[x]
   
   biteavg = biteavg / len(size)
   last = []


   for x in range(len(size)):
      if size[x] > biteavg :
         last.append(checklist[x])

   if len(last) == 1:
      checklist[9] = 1

   mycheck.sort(reverse=True)

   if len(last) >= 2:
      if last[0] > 2*last[1]:
         checklist[9] = 1

   print(checklist)


def process_check(path,filename):
   prolist = [0 for _ in range(5)]
   uname = getpass.getuser()
   path1 = path
   myname = filename
   def fileop(path1,myname):
      os.system(path1+'/'+myname)
      
   th1 = Thread(target=fileop, args=(path1,myname))

   th1.start()

   time.sleep(2)

   while True: 
      proclist = []
      for proc in psutil.process_iter():
         try:
            # 프로세스 이름, PID값 가져오기
            processName = proc.name()
            proclist.append(processName)
            
         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):   #예외처리
            pass

      if "cmd.exe" in proclist:
         prolist[0] = 1
      if "iexplore.exe" in proclist:
         prolist[1] = 1
      if "powershell.exe" in proclist:
         prolist[2] = 1
      if "gswin32c.exe" in proclist:
         prolist[3] = 1
      if "gbb.exe" in proclist:
         prolist[3] = 1

      os.chdir("C:\\Users\\"+uname+"\\AppData\\Local\\Temp\\Hnc\\BinData")
      filecheck1 = os.listdir("./")
      if len(filecheck1) == 0:
         print('\n')
      else:
         for i in range(len(filecheck1)):
            if ".eps" or ".PS" in filecheck1[i]:
               prolist[4] = 1

      if "Hwp.exe" in proclist:
         continue
      else:
         break   
   
   print(prolist)




print("-------------------choose your file----------------------")

root = tkinter.Tk()
root.withdraw()
dir_path = filedialog.askdirectory(parent=root,initialdir="./",title='Please select a directory')
filenames = os.listdir(dir_path)
for i in range(len(filenames)):
   print(i+1,'.',filenames[i])
num1 = int(input("choose number(if 0 == finish) : ")) 
if num1 == 0:
   print("Gooooooooooooooood bye")
   time.sleep(1)
   sys.exit()
else:
   print("start something")
   hex_check(dir_path,filenames[num1 - 1])
   # process_check(dir_path,filenames[num1 - 1])
