import threading
print_lock = threading.Lock()
# Questo mi permette di creare un lock condiviso tra thread in maniera
# da lockare la stampa sul terminale e permettere ad ogni thread di stampare
# tutti i suoi steps prima di farli stampare ad un altro thread