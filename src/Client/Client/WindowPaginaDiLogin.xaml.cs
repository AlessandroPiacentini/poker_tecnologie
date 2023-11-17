using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace Client
{
    /// <summary>
    /// Logica di interazione per WindowPaginaDiLogin.xaml
    /// </summary>
    public partial class WindowPaginaDiLogin : Window
    {
        private TcpClient client;
        private NetworkStream stream;
        private String messaggioRicevuto;

        public WindowPaginaDiLogin()
        {
            InitializeComponent();
        }

        //Invio di un messaggio al Server
        private void InvioDati(String messaggio)
        {
            try
            {
                client = new TcpClient("ServerIPAddress", 666); // Sostituisci "ServerIPAddress" con l'indirizzo IP del server e ServerPort con la porta del server
                stream = client.GetStream();

            }
            catch (Exception ex)
            {
                MessageBox.Show($"Errore nella connessione al server: {ex.Message}");
            }

            try
            {
                if (client != null && client.Connected)
                {
                    byte[] data = Encoding.UTF8.GetBytes(messaggio+";");
                    stream.Write(data, 0, data.Length);
                }
                else
                {
                    MessageBox.Show("Connessione non attiva.");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Errore nell'invio dei dati al server: {ex.Message}");
            }
        }

        //ricezione di messaggio
        private String RicezioneDati()
        {
            try
            {
                if (stream.DataAvailable)
                {
                    byte[] buffer = new byte[1024]; // Dimensione del buffer per memorizzare i dati ricevuti
                    int bytesRead = stream.Read(buffer, 0, buffer.Length); // Leggi i dati ricevuti nella connessione TCP

                    if (bytesRead > 0)
                    {
                        string receivedData = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                        // Restituisci i dati ricevuti
                        return receivedData;
                    }
                }
                else
                {
                    // Nessun dato disponibile al momento, restituisci una stringa vuota o un valore nullo
                    return string.Empty;
                }
            }
            catch (Exception ex)
            {
                // Gestisci l'eccezione
                Console.WriteLine("Errore durante la ricezione dei dati: " + ex.Message);
            }

            // In caso di errori o dati non disponibili, restituisci una stringa vuota o un valore nullo
            return string.Empty;
        }

        //Richiesta di entrare nel gioco al server
        private void buttonEntra_Click(object sender, RoutedEventArgs e)
        {
            InvioDati("entrare");
            if (RicezioneDati()=="connesso")
            {
                RichiestaSuccesso();
            }
            else
            {
                RichiestaFallita();
            }
        }

        //Se la richiesta viene accettata
        private void RichiestaSuccesso()
        {
            // Creazione di un'istanza della terza finestra (finestra di gioco)
            WindowDiGioco WindowDiGioco = new WindowDiGioco();

            // Mostra la nuova finestra
            WindowDiGioco.Show();
            this.Close();
        }

        //Se la richiesta non viene accettata
        private void RichiestaFallita()
        {
            //esce un messaggio di attesa dove comparira un counter
            //OPZIONI DUE:
            //OPZIONE 1 - rimane in coda e appena e disponibile una partita entra
            //OPZIONE 2 - alla fine del counter devi schiacciare entra
        }

    }
}
