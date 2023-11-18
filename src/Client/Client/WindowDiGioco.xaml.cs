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
    /// </summary>
    public partial class WindowDiGioco : Window
    {
        private TcpClient client;
        private NetworkStream stream;

        public WindowDiGioco(TcpClient tcpClient, NetworkStream tcpStream)
        {
            InitializeComponent();
            client = tcpClient;
            stream = tcpStream;
        }

        private void GiocatoriSedutiAlTavolo()
        {

        }
        private void SetupPartita()
        {
            /*for (int i = 0; i < 53; i++)
            {
                if(carta == i)
                {
                    img[i] = immagineresourcei;
                }
            
            }*/
        }
        //Permette l'invio di dati al server
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
                return response.Trim(); // Rimuove eventuali spazi bianchi
            }
            catch (Exception e)
            {
                Console.WriteLine("Errore nella ricezione dei dati: " + e);
                return "err";
            }
        }
    }
}
