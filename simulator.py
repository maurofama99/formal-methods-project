import os
from xml.etree import ElementTree as ET

# Definisci il percorso del tuo file XML
xml_file = 'SMC_Lego_Mindstorms_Production_Plant_deadlock_verification.xml'

# Funzione per modificare i parametri nel file XML
def change_xml_params(file_path, param1_value, param2_value, param3_value):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Modifica i valori dei parametri nel XML
    param1 = root.find('param1')
    param2 = root.find('param2')
    param3 = root.find('param3')
    param1.text = str(param1_value)
    param2.text = str(param2_value)
    param3.text = str(param3_value)

    tree.write(file_path)

# Funzione per eseguire il comando verifyta
def launch_verifyta():
    command = './home/maurofama/Documents/Uni/4th_sem/Formal Methods/uppaal64-4.1.26-2/bin-Linux/verifyta s -o2 /home/maurofama/Documents/Uni/4th_sem/Formal Methods/project/formal-methods-project/SMC_Lego_Mindstorms_Production_Plant_deadlock_verification.xml'  # Comando verifyta
    os.system(command)

def main():
    # Esegui il loop attraverso i valori dei parametri e esegui il comando verifyta
    for param1_value in range(1, 11):
        for param2_value in range(1, 11):
            for param3_value in range(1, 11):
                # Chiamata alla funzione per modificare l'XML
                change_xml_params(xml_file, param1_value, param2_value, param3_value)

                # Chiamata alla funzione per eseguire verifyta
                launch_verifyta()

if __name__ == "__main__":
    main()

