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
    /// Logica di interazione per WindowDiGioco.xaml
    /// Qua si svolgono tutte le operazioni di visualizzazione di gioco e l'invio delle scelte di gioco al server
    /// </summary>
    public partial class WindowDiGioco : Window
    {
        private TcpClient client;
        private NetworkStream stream;

        // Dizionario per tenere traccia dei gruppi di immagini con i loro nomi
        Dictionary<string, List<string>> ImmaginiCarteGiocatori = new Dictionary<string, List<string>>();

        //Array<Giocatore> ListaGiocatori = new System.Array<Giocatore> ();
        public WindowDiGioco(TcpClient tcpClient, NetworkStream tcpStream)
        {
            InitializeComponent();
            client = tcpClient;
            stream = tcpStream;

            //Assegnazione grafica delle carte hai giocatori
            AssegnazioneCarteGrafica();

            IniziaGioco();
        }

        private void IniziaGioco()
        {
            //continua fino a quando il gioco non è finito
            SetupIniziale();
        }
        private void SetupIniziale()
        {
            InvioDati("Inizio_Carte");
            String[] carte = datiSplittati();

            if (ImmaginiCarteGiocatori.ContainsKey(carte[0]))
            {
                if (ImmaginiCarteGiocatori[carte[0]].Count > 0)
                {
                    //ImmaginiCarteGiocatori[carte[0]][0] = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + d + ".jpg"));
                }
                foreach (String c in carte)
                {
                    for (int i = 0; i < 14; i++)
                    {
                        if (c == i.ToString())
                        {
                            img0.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + i + ".jpg"));
                            img1.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "//immagini/" + i + ".jpg"));
                        }
                    }
                }
            }
        }

        //aggiunge al dizionario Le carte (gli id delle immagini) ai rispettivi giocatori
        private void AssegnazioneCarteGrafica()
        {
            List<string> giocatore1 = new List<string>
            {
                "path/1.jpg",
                "path/2.jpg",
            };

            ImmaginiCarteGiocatori.Add("Giocatore1", giocatore1);

            List<string> giocatore2 = new List<string>
            {
                "path/3.jpg",
                "path/4.jpg",
            };

            ImmaginiCarteGiocatori.Add("Giocatore2", giocatore2);

            List<string> giocatore3 = new List<string>
            {
                "path/5.jpg",
                "path/6.jpg",
            };

            ImmaginiCarteGiocatori.Add("Giocatore3", giocatore3);

            List<string> giocatore4 = new List<string>
            {
                "path/7.jpg",
                "path/8.jpg",
            };

            ImmaginiCarteGiocatori.Add("Giocatore4", giocatore4);

            List<string> giocatore5 = new List<string>
            {
                "path/9.jpg",
                "path/10.jpg",
            };

            ImmaginiCarteGiocatori.Add("Giocatore5", giocatore5);

            List<string> giocatore6 = new List<string>
            {
                "path/11.jpg",
                "path/12.jpg",
            };

            ImmaginiCarteGiocatori.Add("Giocatore6", giocatore6);

            List<string> giocatore7 = new List<string>
            {
                "path/13.jpg",
                "path/14.jpg",
            };

            ImmaginiCarteGiocatori.Add("Giocatore7", giocatore7);
        }

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
    }
}
