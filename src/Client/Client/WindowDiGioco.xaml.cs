using System;
using System.Collections.Generic;
using System.Data.SqlTypes;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Linq.Expressions;
using System.Net;
using System.Net.Sockets;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading;
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
using System.Xml;
using System.Xml.Linq;

namespace Client
{
    /// <summary>
    /// Logica di interazione per WindowDiGioco.xaml
    /// Qua si svolgono tutte le operazioni di visualizzazione di gioco e l'invio delle scelte di gioco al server
    /// 
    /// REGOLE GIOCO:
    /// Devi sopravvivere in 4 turni
    /// e alla fine di questi 4 turni devi avere la mano piu forte degli altri giocatori
    /// per rimanere in vita devi puntare
    /// se non lo fai devi lasciare il tavolo
    /// Puoi skippare la decisione che poi andrà al compagno alla tua sinistra
    /// </summary>
    public partial class WindowDiGioco : Window
    {
        //Variabili

        List<Player> Players;
        int GamePhaseCount;
        List<int> BoardCards;

        static string info_del_server = string.Empty;
        int posto;
        int turn;

        private TcpClient client;
        public NetworkStream stream;

        //Costruttore
        public WindowDiGioco(TcpClient tcpClient, int _posto, NetworkStream _stream)
        {
            InitializeComponent();

            posto = _posto;
            client = tcpClient;
            stream = _stream;

            // Aggiungi un gestore per l'evento Loaded
            Loaded += WindowDiGioco_Loaded;
            ContentRendered += WindowDiGioco_ContentRendered;

        }
        
        //Metodi in fase di caricamento della finestra
        private void WindowDiGioco_ContentRendered(object sender, EventArgs e)
        {
            // Questo evento viene chiamato quando il contenuto della finestra è stato reso e tutti i componenti sono pronti
            inizio_gioco();
        }
        private void WindowDiGioco_Loaded(object sender, RoutedEventArgs e)
        {
            // La funzione che vuoi chiamare quando la finestra è caricata
        }

        //Altre variabili
        int pot;
        int carta1;
        int carta2;
        bool is_my_turn = false;


        //Metodo inizia gioco
        public  void inizio_gioco()
        {
            while (is_my_turn == false)
            {
                Application.Current.Dispatcher.Invoke(DispatcherPriority.Background,
                                          new Action(delegate { }));
                Attendi_info_server();
                foreach (Player p in Players)
                {
                    if (posto == p.posto)
                    {
                        Console.Write(carta1 + " " + carta2);
                        carta1 = p.carta1;
                        carta2 = p.carta2;

                        //Definito il valore massimo della puntata
                        SliderSoldi.Maximum = p.soldi;

                        //Nome del giocatore
                        NomeGiocatore.Content = p.name;
                    }

                    //Dato che se questo client è il giocatore 2 non uscirà mai dal ciclo e quindi non si vedra niente in finestra

                    if (posto == turn + 1)
                    {
                        is_my_turn = true;
                    }

                }

                disegnaCarteGiocatori(posto, carta1, carta2);
                disegna_puntate();
                CarteSulTavolo();
                label_pot.Content = pot;
            }


        }

        //Metodo Attendi Info
        private void Attendi_info_server()
        {
            //Console.WriteLine($"Il server è in ascolto su {ipAddress}:{port}");


            // Accettare una connessione client

            Console.WriteLine("Client connesso!");


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

                // Decodificare il messaggio ricevuto
                string receivedMessage = Encoding.ASCII.GetString(message, 0, bytesRead);
                info_del_server = receivedMessage;

                Console.WriteLine($"Messaggio ricevuto: {receivedMessage}");


                stream.Flush();
            }
            if (info_del_server.Split(';')[0]=="winner")
            {
                if (int.Parse(info_del_server.Split(';')[1]) == posto)
                {
                    MessageBox.Show("hai vinto");
                }
                else
                {
                    MessageBox.Show("hai perso");

                }
                MainWindow window = new MainWindow();
                window.Show();
                this.Close();
            }
            else
            {
                parseXML(info_del_server);
            }

        }
        //Metodo Parse XML
        private void parseXML(String stringa)
        {
            XDocument xmlDoc = XDocument.Parse(stringa);



            pot = int.Parse(xmlDoc.Element("root").Element("pot").Value);
            GamePhaseCount = int.Parse(xmlDoc.Element("root").Element("game_phase_count").Value);
            turn = int.Parse(xmlDoc.Element("root").Element("turn").Value);
            BoardCards = xmlDoc.Element("root")
                .Element("board_cards")
                .Elements("item")
                .Select(item => int.Parse(item.Value))
                .ToList();
            Players = xmlDoc.Element("root")
                .Element("players")
                .Elements("Player")
                .Select(player => new Player(player.Element("name").Value, int.Parse(player.Element("card1").Value), int.Parse(player.Element("card2").Value), int.Parse(player.Element("bet").Value), int.Parse(player.Element("chips").Value), player.Element("turn").Value, player.Element("blind").Value, Boolean.Parse(player.Element("seated").Value), int.Parse(player.Element("position").Value))).ToList();


        }
        

        //Metodi disegna

        //Metodo Disegna puntate
        private void disegna_puntate()
        {
            foreach (Player p in Players)
            {
                string g = "giocatore" + p.posto.ToString();
                // Trova la Grid con il nome gruppo1 all'interno del tuo controllo o finestra
                Grid giocatore = (Grid)FindName(g);
                if (giocatore != null)
                {
                    foreach (var controllo in giocatore.Children)
                    {
                        if (controllo is Label l)
                        {
                            l.Content = p.puntata;
                        }
                    }
                }
                if (p.posto == posto)
                {
                    soldi_giocatore.Content = "Hai: " + p.soldi.ToString();
                }
            }

        }

        //Metodo disegna carte giocatori
        private void disegnaCarteGiocatori(int posto, int carta1, int carta2)
        {

            string g = "giocatore" + posto.ToString();
            // Trova la Grid con il nome gruppo1 all'interno del tuo controllo o finestra
            Grid giocatore = (Grid)FindName(g);

            //Variabili utili
            Image immagine1 = null;
            Image immagine2 = null;

            //Cambiamenti
            if (giocatore != null)
            {
                int x = 0;
                foreach (var controllo in giocatore.Children)
                {
                    if (controllo is Image immagine)
                    {
                        if (x == 0)
                        {
                            immagine.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + carta1 + ".jpg"));

                        }
                        else
                        {

                            immagine.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + carta2 + ".jpg"));
                        }
                        x++;
                    }
                }
            }
            // Chiudi le altre carte dei giocatori avversari

            for (int i = 1; i < Players.Count + 1; i++)
            {
                if (i != posto)
                {
                    g = "giocatore" + i;
                    // Trova la Grid con il nome gruppo1 all'interno del tuo controllo o finestra
                    Grid giocatoreAvversario = (Grid)FindName(g);



                    //Cambiamenti
                    if (giocatore != null)
                    {
                        int x = 0;
                        foreach (var controllo in giocatoreAvversario.Children)
                        {
                            if (controllo is Image immagine)
                            {
                                if (x == 0)
                                {
                                    immagine.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/53.jpg"));

                                }
                                else
                                {

                                    immagine.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/53.jpg"));
                                }
                                x++;
                            }
                        }
                    }
                }
            }


        }

        //Metodi discegna carte sul tavolo
        private void CarteSulTavolo()
        {


            // Trova la Grid con il nome carte del tavolo
            Grid giocatore = (Grid)FindName("tavolo");
            //if (BoardCards.Count > 0)
            //{
            //    imgTavolo1.Opacity = 0;
            //    imgTavolo2.Opacity = 0;
            //    imgTavolo3.Opacity = 0;
            //    imgTavolo4.Opacity = 0;
            //    imgTavolo5.Opacity = 0;

            //}

            if (BoardCards.Count > 0)
            {
                imgTavolo1.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + BoardCards[0] + ".jpg"));
                imgTavolo2.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + BoardCards[1] + ".jpg"));
                imgTavolo3.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + BoardCards[2] + ".jpg"));
                //Le altre carte le rendo trasparenti
            }
            if (BoardCards.Count > 3)
            {
                imgTavolo4.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + BoardCards[3] + ".jpg"));
            }
            if (BoardCards.Count > 4)
            {
                imgTavolo5.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + BoardCards[4] + ".jpg"));
            }
        }


        //Metodi bottoni

        //Metodi Click bottone puntata
        private void buttonPuntata_Click(object sender, RoutedEventArgs e)
        {
            string puntata = txtPuntata.Text;
            try
            {
                byte[] message = Encoding.ASCII.GetBytes("add;" + puntata);
                stream.Write(message, 0, message.Length);
                is_my_turn = false;
                inizio_gioco();
            }
            catch (Exception a)
            {
                Console.WriteLine("Errore: " + a);
            }


        }
        //Metodi Click bottone Fold
        private void buttonFold_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                byte[] message = Encoding.ASCII.GetBytes("fold;");
                stream.Write(message, 0, message.Length);
                is_my_turn = false;

                inizio_gioco();
            }
            catch (Exception a)
            {
                Console.WriteLine("Errore: " + a);
            }
        }
        //Metodi Click bottone Check
        private void buttonCheck_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                byte[] message = Encoding.ASCII.GetBytes("see;");
                stream.Write(message, 0, message.Length);
                is_my_turn = false;
                inizio_gioco();
            }
            catch (Exception a)
            {
                Console.WriteLine("Errore: " + a);
            }
        }

        //Metodo di cambiamento del valore dello slider
        private void Slider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            //txtPuntata.Text = e.NewValue.ToString();

            double newValue = Math.Round(e.NewValue / 5) * 5; // Arrotonda il valore al multiplo di 5 più vicino
            txtPuntata.Text = newValue.ToString();
            SliderSoldi.Value = newValue; // Imposta il valore dello Slider al multiplo di 5 più vicino
        }
    }
}
