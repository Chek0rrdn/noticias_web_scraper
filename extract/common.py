import yaml
import signal, sys, time

__config = None

def config():
    global __config
    if not __config:

        with open('./config.yaml', mode='r') as f:
            __config = yaml.safe_load(f)

    return __config


##MEDIR TIEMPO
def tiempo_de_ejecucion(func):
    def envoltura(*args, **kwargs):
        tiempo_inicial = time.time()
        func(*args, **kwargs)
        tiempo_final = time.time()
        tiempo_transcurrido = tiempo_final-tiempo_inicial
        tiempo_transcurrido = round(tiempo_transcurrido, 3)
        print(f"Transcurrieron: {tiempo_transcurrido} segundos")

    return envoltura


#MANEJO DEL Ctrl. + C
def def_handler(sig, frame):
    print("\nSaliendo...\n")
    sys.exit()

signal.signal(signal.SIGINT, def_handler)