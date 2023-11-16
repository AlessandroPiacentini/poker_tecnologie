using System;
using System.Collections.Generic;
using System.Linq;
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
        public WindowPaginaDiLogin()
        {
            InitializeComponent();
        }
        private void InvioDati()
        {
            try
            {
                client = new TcpClient("ServerIPAddress", ServerPort); // Sostituisci "ServerIPAddress" con l'indirizzo IP del server e ServerPort con la porta del server
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
                    byte[] data = Encoding.UTF8.GetBytes(MessageTextBox.Text);
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

        private void RicezioneDati()
        {

        }
    }
}
