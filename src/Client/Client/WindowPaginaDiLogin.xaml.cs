using Microsoft.VisualBasic.FileIO;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Markup;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using static System.Net.Mime.MediaTypeNames;


namespace Client
{
    /// <summary>
    /// Logica di interazione per WindowPaginaDiLogin.xaml
    /// Questa pagina invece ha 4 compiti: instaurare una connessione, prendere il nome del giocatore, i soldi e verificare se il tavolo è pieno o no.
    /// </summary>
    public partial class WindowPaginaDiLogin : Window
    {

        //Variabili
        public TcpClient client;
        public NetworkStream stream;

        public string ipclient;
        public int portclient;

        //Costruttore
        public WindowPaginaDiLogin()
        {
            InitializeComponent();
            txtRicerca.Visibility = Visibility.Collapsed;

            txtDiAttesa.Visibility = Visibility.Collapsed;

            

            txtDiAttesa.Opacity = 0;


        }
        string ip_server;
        int port_server;
        private void get_ip_server(){
            using (StreamReader sr = new StreamReader("../config.csv"))
            {
                ip_server = sr.ReadLine().Split(':')[1];
                port_server = int.Parse(sr.ReadLine().Split(':')[2]);
            }
        }

        //Metodo Invio di un messaggio al Server
        private void InvioDati(String messaggio)
        {
            client = new TcpClient(ip_server, port_server);
            stream = client.GetStream();
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



        //Metodo ricezione di messaggio
        private String RicezioneDati()
        {
            try
            {
                byte[] buffer = new byte[1024];
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                String response = Encoding.ASCII.GetString(buffer, 0, bytesRead);
                return response.Trim(); // Rimuove eventuali spazi bianchi
            }
            catch (Exception e)
            {
                Console.WriteLine("Errore nella ricezione dei dati: " + e);
                return "err";
            }
        }

        //Metodo Richiesta di entrare nel gioco al server
        private async void buttonEntra_Click(object sender, RoutedEventArgs e)
        {
            txtDiAttesa.Visibility = Visibility.Visible;
            txtRicerca.Visibility = Visibility.Visible;
            String dati = "";

            //Controllo se ce scritto qualcosa
            if (!string.IsNullOrEmpty(txtNome.Text) && !string.IsNullOrEmpty(txtNome.Text))
            {
                if (!string.IsNullOrEmpty(txtNome.Text))
                {
                    if (!string.IsNullOrEmpty(txtSoldi.Text))
                    {
                        //Cotrolli se i soldi sono solo numeri
                        if (Regex.IsMatch(txtSoldi.Text, @"^\d+$"))
                        {
                            // Il testo contiene solo numeri
                            Console.WriteLine("Il testo contiene solo numeri: " + txtSoldi);

                            dati = txtNome.Text + ";" + txtSoldi.Text;    // Invia: (nome e soldi)
                            InvioDati("entry;" + dati);
                        }
                        else
                        {
                            Console.WriteLine("Il testo contiene caratteri diversi dai numeri");
                            MessageBox.Show("Inserisci solo numeri nel campo Soldi.");

                            txtSoldi.Text = "";

                            return; // Esci dal metodo se il testo non contiene solo numeri
                        }
                    }
                    else
                    {
                        // Il TextBox è vuoto
                        MessageBox.Show("Inserisci i soldi");
                        return; // Esci dal metodo se il testo non contiene solo numeri
                    }
                }
                else
                {
                    // Il TextBox è vuoto
                    MessageBox.Show("Inserisci il nome");
                    return; // Esci dal metodo se il testo non contiene solo numeri
                }
            }
            else
            {
                // Il TextBox è vuoto
                MessageBox.Show("Inserisci il nome e soldi");
                return; // Esci dal metodo se il testo non contiene solo numeri
            }

            // Aspetta fino a quando non è di nuovo il tuo turno
            String messaggio = await AttendiRisposta();

            if (messaggio.Split(';')[0] == "ok")
            {

                RichiestaSuccesso();
            }
            else
            {
                RichiestaFallita();
            }
        }
        private async void set_socket_server()
        {
            string receivedMessage = "";


            // Accettare una connessione client


            byte[] message = new byte[4096];
            int bytesRead;


            bytesRead = 0;

            try
            {
                bytesRead = stream.Read(message, 0, 4096);
            }
            catch
            {

            }

            if (bytesRead != 0)
            {
                txtDiAttesa.Opacity = 75;
                txtDiAttesa.Text = "Giocatori entrati:";

                // Decodificare il messaggio ricevuto
                receivedMessage = Encoding.ASCII.GetString(message, 0, bytesRead);
                Console.WriteLine($"Messaggio ricevuto: {receivedMessage}");

                stream.Flush();
            }

            Console.Write(receivedMessage);
            connessione_a_nuova_socket_server(receivedMessage);

        }



        //Metodo che connette il client alla nuova socket del server
        public void connessione_a_nuova_socket_server(string receivedMessage)
        {


            string ip = receivedMessage.Split(';')[0];
            int port = int.Parse(receivedMessage.Split(';')[1]);
            client = new TcpClient(ip, port); // Connessione al server Java sulla porta 8080
            stream = client.GetStream();
            try
            {
                byte[] message = Encoding.ASCII.GetBytes("connesso");
                stream.Write(message, 0, message.Length);
            }
            catch (Exception e)
            {
                Console.WriteLine("Errore: " + e);
            }
        }



        //Metodo se la richiesta viene accettata
        private void RichiestaSuccesso()
        {
            // Creazione di un'istanza della terza finestra (finestra di gioco)

            set_socket_server();

            WindowDiGioco WindowDiGioco = new WindowDiGioco(client, posto, stream);

            // Mostra la nuova finestra
            WindowDiGioco.Show();
            this.Close();
        }

        //Metodo Se la richiesta non viene accettata
        private void RichiestaFallita()
        {
            //esce un messaggio di attesa dove comparira un counter
            //OPZIONI DUE:
            //OPZIONE 1 - rimane in coda e appena e disponibile una partita entra
            //OPZIONE 2 - alla fine del counter devi schiacciare entra
        }
        
        //Variabile posto
        int posto;

        //Metodo che attenda una risposta dal server
        private async Task<String> AttendiRisposta()
        {
            String[] risposta;

            while (true)
            {

                risposta = RicezioneDati().Split(';'); // Dividi utilizzando il punto e virgola come separatore
                if (risposta.Length > 0 && risposta[0] == "ok")
                {
                    posto = int.Parse(risposta[1]);
                    break; // Esci dal ciclo quando la risposta è "ok"
                }

                // Aggiungi un ritardo per evitare un ciclo troppo veloce
                await Task.Delay(1000); // Ritardo di 1 secondo (1000 millisecondi)
            }


            return risposta.Length > 0 ? risposta[0] : ""; // Restituisci il primo elemento se presente, altrimenti una stringa vuota
        }
    }
}
