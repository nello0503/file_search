"""
il seguente programma fa le seguenti operazioni:

1) richiede all'utente 3 parametri di input:

    a) una parola da cercare (es. correlazione) PARAM1

	b) una directory di partenza per la ricerca 
		(es. in PC windows c:/Documenti
                 es. in PC Linux/MAx /Users/andrea/Documents) PARAM2
    c) una directory di output (es. DocumentiRisultatiRicerca)
		PARAM3

2) cercare PARAM1 in tutti i file presenti in PARAM2 e in tutte le sottodirectory.

    In particolare la ricerca dovrà riguardare il nome del file
    (es. se un file si chiama CorrelazioneLineare.dat allora dovrà essere un 
    output della ricerca).

    Qualora il nome del file non contiene la parola specificata in PARAM1
    lo studente può scrivere delle funzioni che cercano PARAM1 nel contenuto 
    del file. In particolare lo studente può proporre funzioni che:

    - effettuano una ricerca byte a byte, con il file considerato un file
    di testo o comunque aperto in modalità binaria.

    - effettuano una ricerca dopo avere riconosciuto nel file una certa 
    struttura (es. file PDF) ed avere gestito opportunamente tale struttura.

    Esempi di strutture gestibili sono il PDF, il DOC (Microsoft word del
    pkt OFFICE), ma anche altri a scelta dello studente. 


    3) tutti i file che contengono, nel senso indicato dal punto 2) PARAM1
    dovranno essere copiati nella directory specificata in PARAM3

    Tutto ciò che non è specificato nell'esercizio è lasciato alla decisione
    dello studente. Es. la directory specificata in PARAM3 può pre-esistere
    rispetto ad una esecuzione del programma oppure può non esistere. E'
    lasciata alla studente la gestione dei due casi.
  """  

import fnmatch
import os
import shutil
import re
from pypdf import PdfReader # type: ignore
from docx import Document # type: ignore


#La seguente funzione elimina i file presenti dalle esecuzioni precedenti nella cartella dei risultati trovati
def erase_memory (erasepath):
    for nome_file in os.listdir(erasepath):
        percorso = os.path.join(erasepath, nome_file)
        if os.path.isfile(percorso):
            os.remove(percorso)

#La seguente funzione ricerca la parola all' interno di un file .pdf
def filename_inner_pdf_search(word, path, final):
    try:
            reader = PdfReader(path)
            for page in reader.pages:
                text = page.extract_text() or ""
                if word in text:  
                      shutil.copy2(path, final)
                      trovati.add(path)
                      break               
    except Exception as e:
            print(f"Errore nella lettura PDF {path}: {e}")
       
#La seguente funzione ricerca la parola all' interno di un file .txt
def filename_inner_txt_search(word, path, final):
        try:
             with open(path, "r", encoding="utf-8", errors="ignore") as f:         
                    for riga in f:
                        if word in riga:
                            shutil.copy2(path, final) 
                            trovati.add(path)                       
                            break                                  
        except (IOError, OSError) as e:
             print(f"Impossibile leggere: {path} ({e})")

#La seguente funzione ricerca la parola all' interno di file .docx
def filename_inner_docx_search(word, path, final):
    doc = Document(path)  
    # Paragrafi
    for i, p in enumerate(doc.paragraphs):
        if word in p.text:
            shutil.copy2(path, final)
            trovati.add(path)
            break  


#La seguente funzione ricerca la parola all' interno dei file nel caso in cui la ricerca del nome non ha prodotto risultati
def word_inner_search(word):
    for root, dirs, files in os.walk(start_directory):
        for filename in files:                                  
            #caso file PDF
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(root, filename) 
                filename_inner_pdf_search(word, full_path, output_directory)
            #caso file TXT
            if filename.lower().endswith(".txt"):
                full_path = os.path.join(root, filename) 
                filename_inner_txt_search(word, full_path, output_directory) 
            #caso fila DOCX
            if filename.lower().endswith(".docx"):
                full_path = os.path.join(root, filename) 
                filename_inner_docx_search(word, full_path, output_directory) 
    print(f"La ricerca ha prodotto {len(trovati)} risultati ")
    print("-" * 50)


#La seguente funzione copia ed incolla i file quando il nome corrisponde con la parola digitata
def filename_search():  
    file_name = input("Digita il nome del file (es. *.py): ")
    #Cancello i file presenti
    erase_memory(output_directory)
    for root, dirs, files in os.walk(start_directory):
        for filename in files:
    #Verifico che il nome del file fa match con PARAM1
                if fnmatch.fnmatch(filename, file_name): 
                    full_path = os.path.join(root, filename) 
    #Il nome del file fa match, quindi va ricopiato     
                    shutil.copy2(full_path, output_directory)  
                    trovati.add(full_path)
    print(f"La ricerca ha prodotto {len(trovati)} risultati")
    print("-" * 50)               

    #La ricerca non ha prodotto risultati          
    if len(trovati) == 0:
        #controllo della wildcard * nell' input
        if("*" in file_name):
            word = input("❌Non ho trovato file con quel nome, digita la parola senza wildcard: ")
            word_inner_search(word)       
        else:
             print("Procedo con la ricerca interna ai file")            
             word_inner_search(file_name)

# --- INPUT directory di input ---             
while True:
    start_directory = input("Inserisci la directory di partenza: ").strip()

    if not start_directory:
        print("❌ La directory di partenza non può essere vuota.")
        continue

    if not os.path.isdir(start_directory):
        print("❌ La directory di partenza non esiste o non è una cartella.")
        continue

    break


# --- INPUT directory di output ---
while True:
    output_directory = input("Inserisci la directory di output: ").strip()


    # se non esiste, la creo
    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
            print(f"📁 Cartella creata: {output_directory}")
        except OSError as e:
            print(f"❌ Impossibile creare la cartella: {e}")
            continue

    # controllo che sia davvero una cartella
    if not os.path.isdir(output_directory):
        print("❌ Il percorso di output non è una cartella.")
        continue

    break


print("\nDirectory di partenza:", start_directory)
print("Directory di output:", output_directory)
print("-" * 50)
trovati = set()
filename_search()



