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
    /// Logica di interazione per WindowAttesa.xaml
    /// </summary>
    public partial class WindowAttesa : Window
    {
        public TcpClient client;
        public NetworkStream stream;
        int posto;
        public WindowAttesa(TcpClient client, NetworkStream stream, int posto)
        {
            InitializeComponent();
            ContentRendered += WindowDiGioco_ContentRendered;
            this.client = client;
            this.posto = posto;
            this.stream = stream;
        }

        private void WindowDiGioco_ContentRendered(object sender, EventArgs e)
        {
            set_socket_server();

            WindowDiGioco WindowDiGioco = new WindowDiGioco(client, posto, stream);

            // Mostra la nuova finestra
            WindowDiGioco.Show();
            this.Close();
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

                // Decodificare il messaggio ricevuto
                receivedMessage = Encoding.ASCII.GetString(message, 0, bytesRead);
                Console.WriteLine($"Messaggio ricevuto: {receivedMessage}");

                stream.Flush();
            }

            Console.Write(receivedMessage);
            connessione_a_nuova_socket_server(receivedMessage);

        }
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
    }
}
