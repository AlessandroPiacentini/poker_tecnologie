using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Interop;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace Client
{
    /// <summary>
    /// Logica di interazione per WindowDiGioco.xaml
    /// Qua si svolgono tutte le operazioni di visualizzazione di gioco e l'invio delle scelte di gioco al server
    /// 
    /// REGOLE GIOCO:
    /// Devi soppravvivere in 4 tunri
    /// e alla fine di questi 4 turni devi avere la mano piu forte degli altri giocatori
    /// per rimanere in vita devi puntare
    /// se non lo fai devi lasciare il tavolo
    /// Puoi skippare la decisione che poi andrà al compagno alla tua sinistra
    /// </summary>
    public partial class WindowDiGioco : Window
    {
        //Connessioni TCP Client e Server
        private TcpClient client;
        private NetworkStream stream;

        //Iniziallizzazione piccolo e grande buio
        int grande_buio = 0;
        int piccolo_buio = 0;

        //Contatore dei turni
        int conta = 0;

        public WindowDiGioco(TcpClient tcpClient, NetworkStream tcpStream)
        {
            InitializeComponent();
            client = tcpClient;
            stream = tcpStream;

            IniziaGioco();
        }
    
        //INIZIO DEL GIOCO
        private void IniziaGioco()
        {
            CarteIniziali();
            CarteSulTavolo();
            addBottoneAlGiocatore();

            if (conta == 4) aggiungiEVisualizzaCarta4();
            if (conta == 5) aggiungiEVisualizzaCarta5();
        }



        //FASI DEL GIOCO

        //Metodo che dice chi iniza
        private void ChiInizia()
        {
            for (int i = 12; i >= 0; i--)
            {
                String nomeGiocatore = "giocatore" + i; // Sostituisci con la logica corretta per ottenere i nomi delle Grid dei giocatori avversari
                Grid giocatore = (Grid)FindName(nomeGiocatore);

                if (giocatore != null)
                {

                    //dice al server il nome del giocatore che Inizia per primo
                    InvioDati("giocatore_che_inizia");
                    if(RicezioneDati()=="dammelo")
                        InvioDati(nomeGiocatore);
                }
            }
        }
        
        //Calcola il piccolo buio
        private void piccoloBuio()
        {
            piccolo_buio = grande_buio / 2;
        }

        //Calcola il grande buoio
        private void grandeBuio()
        {
            //viene calcolato il grande buoi passato dal Server
            InvioDati("grande_buio");
            int grande_buio = int.Parse(RicezioneDati());

            //richiama il metodo piccolo buio
            piccoloBuio();
        }

        //Metodo che dice che lascia il tavolo
        private void abbandonare()
        {
            InvioDati("abbandonare");
    
            //DISATTIVA TUTTO
        }

        //Passo il turno
        private void check()
        {
            InvioDati("Check");
            if (RicezioneDati() == "ok_fermo")
            {
                //disattiva i bottoni
                buttonFold.IsEnabled = false;
                buttonCheck.IsEnabled = false;
                buttonPuntata.IsEnabled = false;
            }
        }

        //Disabilita tutto perchè hai finito il turno
        private void turnoFinito()
        {
            InvioDati("turno_finito");
            if (RicezioneDati() == "ok_fermo")
            {
                //disattiva i bottoni
                buttonFold.IsEnabled = false;
                buttonCheck.IsEnabled = false;
                buttonPuntata.IsEnabled = false;
            }
        }

        //Metodo della puntata che invia al Server
        private void puntata()
        {
            String puntata = "";

            //Metti in una variabile la puntata
            puntata = txtPuntata.Text;

            //invia i soldi della puntata
            InvioDati("puntata");
            if(RicezioneDati() == "ok_puntata")
            {
                String puntataMinima = grande_buio.ToString();
                if (int.Parse(puntata) < int.Parse(puntataMinima))
                {
                    //PUNTATA NON VALIDA MINIMO Di: puntata
                }
                else
                {
                    InvioDati(puntata);
                    //E infine aggiorna il saldo
                    txtSaldo.Text = (int.Parse(txtSaldo.Text) - int.Parse(txtPuntata.Text)).ToString();
                }
            }   
        }
        
       

        //CAMBIAMENTO SUL CAMPO

        //Fa vedere la nuova carta sul tavolo (carta 4)
        private void aggiungiEVisualizzaCarta4()
        {
            InvioDati("pesca");
            String[] carte = datiSplittati();

            //Rendo la immagine di nuovo visibile
            imgTavolo4.Opacity = 0.5;

            //E cambio percorso
            imgTavolo4.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + carte[1] + ".jpg"));
        }

        //Fai vedere la nuova e quinta carta sul tavolo
        private void aggiungiEVisualizzaCarta5()
        {
            InvioDati("pesca");
            String[] carte = datiSplittati();

            //Rendo la immagine di nuovo visibile
            imgTavolo4.Opacity = 0.5;

            //E cambio percorso
            imgTavolo5.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + carte[1] + ".jpg"));
        }



        //METODI PER IL SETUP DEL GIOCO

        //Carte sul tavolo
        private void CarteSulTavolo()
        {
            InvioDati("Carte_Tavolo");
            String[] carte = datiSplittati();

            // Trova la Grid con il nome carte del tavolo
            Grid giocatore = (Grid)FindName("tavolo");

            imgTavolo1.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + carte[0] + ".jpg"));
            imgTavolo2.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + carte[1] + ".jpg"));
            imgTavolo3.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + carte[2] + ".jpg"));

            //Le altre carte le rendo trasparenti
            imgTavolo4.Opacity = 0;
            imgTavolo5.Opacity = 0;
        }

        //Ovvero dai a ciascun giocatore le carte che gli spettano decide dal server
        private void CarteIniziali()
        {
            InvioDati("Inizio_Carte");
            String[] carte = datiSplittati();

            // Trova la Grid con il nome gruppo1 all'interno del tuo controllo o finestra
            Grid giocatore = (Grid)FindName(carte[0]);

            //Variabili utili
            Image immagine1 = null;
            Image immagine2 = null;

            if (giocatore != null)
            {
                int x = 1;
                foreach (var controllo in giocatore.Children)
                { 
                    if (controllo is Image immagine)
                    {
                        // Verifica se si è raggiunto l'ultimo percorso nell'array
                        if (x!=3)
                        {
                            immagine.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + carte[x] + ".jpg"));
                            if (x == 1)
                            {
                                immagine1 = immagine;
                            }
                            else if (x == 2)
                            {
                                immagine2 = immagine;
                            }

                            x++;
                        }
                    }
                }

                // Chiudi le altre carte dei giocatori avversari
                int j = 0;

                for (int i = 0; i < 13; i++)
                {
                    String nomeGridAvversario = "giocatore" + i; // Sostituisci con la logica corretta per ottenere i nomi delle Grid dei giocatori avversari
                    Grid avversario = (Grid)FindName(nomeGridAvversario);

                    if (avversario != null)
                    {

                        Image immagineCopertaAvversario1 = (Image)avversario.FindName("img" + j); // Sostituisci con la logica corretta per ottenere i nomi delle immagini dei giocatori avversari
                        
                        if (immagineCopertaAvversario1 != immagine1 && immagineCopertaAvversario1 != immagine2)
                        {
                            if (immagineCopertaAvversario1 != null)
                            {
                                immagineCopertaAvversario1.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/53.jpg"));
                            }
                        }
                        
                        //aggiunta per la seconda carta
                        j++;
                        Image immagineCopertaAvversario2 = (Image)avversario.FindName("img" + j); // Sostituisci con la logica corretta per ottenere i nomi delle immagini dei giocatori avversari

                        if (immagineCopertaAvversario2 != immagine1 && immagineCopertaAvversario2 != immagine2)
                        {
                            if (immagineCopertaAvversario2 != null)
                            {
                                immagineCopertaAvversario2.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/53.jpg"));
                            }
                        }
                      j++;
                    }
                }

                //Carte al tavolo trasparenti
            }

        }

        //Assegnazione dei bottoni al giocatore
        private void addBottoneAlGiocatore()
        {
            InvioDati("giocatore");
            String[] g = datiSplittati();

            // Supponiamo che 'giocatore' sia il nome di un elemento della UI di tipo Grid
            Grid giocatore = this.FindName(g[0]) as Grid;

            if (giocatore != null)
            {
                giocatore.Children.Add(buttonCheck); // Aggiungi il pulsante alla griglia
                giocatore.Children.Add(buttonFold); // Aggiungi il pulsante alla griglia
                giocatore.Children.Add(buttonFold); // Aggiungi il pulsante alla griglia
            }
        }



        //METODI UTILI DURANTE LA CONNESSIONE TRA CLIENT E SERVER

        //Permette l'invio di dati
        private void InvioDati(String messaggio)
        {
            try
            {
                byte[] message = Encoding.ASCII.GetBytes(messaggio + ";");
                stream.Write(message, 0, message.Length);
            }
            catch (Exception e)
            {
                Console.WriteLine("Errore: " + e);
            }
        }

        //Permette la ricezione di dati dal server
        private String RicezioneDati()
        {
            try
            {
                byte[] buffer = new byte[1024];
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                String response = Encoding.ASCII.GetString(buffer, 0, bytesRead);
                return response.Trim();                                                // Rimuove eventuali spazi bianchi
            }
            catch (Exception e)
            {
                Console.WriteLine("Errore nella ricezione dei dati: " + e);
                return "err";
            }
        }

        //Questo metodo prende i dati dal Server, gli splitta e ritorna un array di quei dati
        private String[] datiSplittati()
        {
            String[] carte;

            String dati = RicezioneDati().ToString(); // Ottieni i dati come stringa
            return carte = dati.Split(';'); // Dividi la stringa utilizzando il punto e virgola come separatoreuna virgola
        }


        //METODI ASCINCORNI PER LA COMUNICAZIONE CON IL SERVER
        //Creazione di un metodo asincrono per l'attesa del messaggio dal server:
        private async Task<String> AttendiTurno()
        {
            string risposta = "";

            while (true)
            {
                risposta = RicezioneDati();
                if (risposta == "il_tuo_turno")
                {
                    break; // Esci dal ciclo quando è di nuovo il tuo turno
                }

                // Aggiungi un ritardo per evitare un ciclo troppo veloce
                await Task.Delay(1000); // Ritardo di 1 secondo (1000 millisecondi)
            }

            return risposta;
        }

        //METODI DEI BOTTONI

        //Se viene schiacciato il tasto del FOLD
        private async void buttonFold_Click(object sender, RoutedEventArgs e)
        {
            abbandonare();
            turnoFinito();

            // Aspetta fino a quando non è di nuovo il tuo turno
            String messaggio = await AttendiTurno();

            // Qui puoi eseguire azioni dopo aver ricevuto il messaggio "il_tuo_turno"
            if (messaggio == "il_tuo_turno")
            {
                // Abilita di nuovo i bottoni
                buttonFold.IsEnabled = true;
                buttonCheck.IsEnabled = true;
                buttonPuntata.IsEnabled = true;
            }
        }

        //Se viene schiacciato il tasto check
        private async void buttonCheck_Click(object sender, RoutedEventArgs e)
        {
            check();
            turnoFinito();

            // Aspetta fino a quando non è di nuovo il tuo turno
            String messaggio = await AttendiTurno();

            // Qui puoi eseguire azioni dopo aver ricevuto il messaggio "il_tuo_turno"
            if (messaggio == "il_tuo_turno")
            {
                // Abilita di nuovo i bottoni
                buttonFold.IsEnabled = true;
                buttonCheck.IsEnabled = true;
                buttonPuntata.IsEnabled = true;
            }
        }

        //Se viene schiacciato il tasto puntata
        private async void buttonPuntata_Click(object sender, RoutedEventArgs e)
        {
            puntata();
            turnoFinito();

            // Aspetta fino a quando non è di nuovo il tuo turno
            String messaggio = await AttendiTurno();

            // Qui puoi eseguire azioni dopo aver ricevuto il messaggio "il_tuo_turno"
            if (messaggio == "il_tuo_turno")
            {
                // Abilita di nuovo i bottoni
                buttonFold.IsEnabled = true;
                buttonCheck.IsEnabled = true;
                buttonPuntata.IsEnabled = true;
            }

        }
    }
}