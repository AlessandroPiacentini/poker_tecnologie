# Poker Texas Hold'em con Comunicazione TCP

Questo progetto implementa un'applicazione di Poker Texas Hold'em che consente a più giocatori di partecipare a una partita tramite comunicazione TCP.

## Funzionalità

- Creazione di un server di gioco che accetta connessioni TCP dai giocatori.
- Gestione delle regole del Poker Texas Hold'em, inclusi i turni di scommesse e la valutazione delle mani dei giocatori.
- Comunicazione bidirezionale tra il server e i giocatori tramite socket TCP.
- Visualizzazione delle informazioni di gioco, come le carte dei giocatori e il montepremi.

## Requisiti di installazione

- Python 3.x
- Libreria socket per la comunicazione

## Istruzioni per l'uso

1. Clonare il repository del progetto:

    ```bash
    git clone https://github.com/AlessandroPiacentini/poker_tecnologie.git
    ```
    modificare il file .config.csv com l'indirizzo giusto del server

2. Avviare il server di gioco:

    ```bash
    python main.py
    ```

3. Avviare l'applicazione client su ogni computer dei giocatori:
    
    ```bash
    call run_client.bat
    ```

4. Seguire le istruzioni visualizzate sull'applicazione client per partecipare alla partita.

## Autori

- Alessandro Piacentini
- Alessandro Aguilar

