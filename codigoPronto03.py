import cv2
import time
import serial
import bluetooth

ser = serial.Serial('/dev/ttyUSB0', 115200)

PORTA = 1
servidor = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
servidor.bind(("", PORTA))
servidor.listen(1)
cliente,endereco = servidor.accept()
print("Conexao realizada com", endereco)

num = 0
limite = 999  
delay = 1

try:
    while True:
        dados = cliente.recv(1024)
        print("Recebido: %s" %dados)
        
        if(dados == b'1'):
            delay = 2.50
        if(dados == b'2'):
            delay = 5
        if(dados == b'3'):
            delay = 7.5
        if(dados == b'4'):
            delay = 10
        if(dados == b'5'):
            delay = 12.5
        if(dados == b'6'):
            delay = 15
            
        if (dados == b'S'):
            print("Parando")
            ser.write(str.encode("<0_0>"))
    
        if (dados == b'F'):
            print("Indo pra Frente")
            print(delay)
            ser.write(str.encode("<0_240>"))
            time.sleep(delay)
            ser.write(str.encode("<0_0>"))
     
        if (dados == b'B'):
            print("Indo pra Trás")
            ser.write(str.encode("<240_0>"))
            time.sleep(delay)
            ser.write(str.encode("<0_0>"))
        
        if (dados == b'T'):
            cap = cv2.VideoCapture(0)
            ret, img = cap.read()
            if num > limite:
                num = limite
            cv2.imwrite('/media/projete3103/F0E9-334E1/Fotos/'+str(num)+'.jpg', img)
            print('Capture '+str(num)+' Successful')
            num += 1
            cap.release()
            
        if (dados == b'C'):
            num = 0
        
        if(dados == b'CB'):
            print("Sair")
            break
    
    ser.write(str.encode("<0_0>"))
    cliente.close()
    servidor.close()
except:
    print("Fora de alcance do celular")
    ser.write(str.encode("<0_240>"))
    time.sleep(10)
    ser.write(str.encode("<0_0>"))


 