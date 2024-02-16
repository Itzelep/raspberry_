from machine import Pin, UART, SPI
import bme280
import sdcard
import uos
import ssd1306
import utime
import mysql.connector
import serial
from datetime import datetime
from utime import sleep



led = Pin(6, Pin.OUT)  # Ajusta el número del pin según tu placa

uart = UART(1,RX= (7), TX = (6), freq = 400000)
i2c_1 = I2C(1, TX = Pin(33), RX = Pin(32))



CS = Pin(13, Pin.OUT)
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
sd = sdcard.SDCard(spi, CS)
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")


# Configura los detalles de la conexión (reemplaza con tus propios valores)
host = "localhost"  # IP de tu PC con XAMPP
user = "root"       # Usuario de la base de datos
password = ""       # Contraseña de la base de datos
database_name = "Temperatura"  # Nombre de la base de datos

# Crea la conexión
conn = mysql.connector.connect(host=host, user=user, passwd=password, database=database_name)
cursor = conn.cursor()

# Configura el puerto serial (ajusta según tu configuración)
ser = serial.Serial('/dev/ttyAMA1', 9600)

while True:
    # Leer datos desde el sensor a través de UART
    data = ser.readline().decode().strip()
    
    # Obtener la fecha y hora actual
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Insertar los datos en la base de datos
    cursor.execute("INSERT INTO Temperatura (fecha, temperatura) VALUES (%s, %s)", (timestamp, float(data)))
    conn.commit()

# Cierra la conexión al final
cursor.close()
conn.close()

while True:
    bme = bme280.BME280(i2c=i2c)
    bmeS = ','.join(bme.values)
    
    led.value(1)
    
    with open("/sd/datos.txt", "w") as file:
        pantalla.text("Abriendo archivo",1,20,1)
        pantalla.show()
        utime.sleep(2)
        pantalla.text("Abriendo archivo",1,20,0)
        pantalla.show()
        file.write(bmeS)
        

    # Leer el archivo desde la tarjeta SD
    with open("/sd/datos.txt", "r") as file:
        pantalla.text("Leyendo archivo",1,20,1)
        pantalla.show()
        utime.sleep(2)
        pantalla.text("Leyendo archivo",1,20,0)
        pantalla.show()
        data = file.read()
        print(data)

    led.value (1) #1 para valor positivo
    utime.sleep(2)
    led.value (0)

    datos = data.split(",")

    

    while True:
        pantalla.text("temp:{}".format(datos[0]), 1,5, 1)
        #pantalla.fill_rect(5,5,123,59,1)
        pantalla.show()
        utime.sleep(1)
        pantalla.text("pres:{}".format(datos[1]), 1,20, 1)
        pantalla.show()
        utime.sleep(1)
        pantalla.text("HR:{}".format(datos[2]), 1,35, 1)
        pantalla.show()
        utime.sleep(1)


