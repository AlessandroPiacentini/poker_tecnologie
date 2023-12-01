using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Runtime.InteropServices.ComTypes;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Markup;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Client
{
    /// <summary>
    /// Logica di interazione per MainWindow.xaml
    /// Questa Finesta è la schermata di gioco e se si vuole giocare basta soltanto che si schiacci gioca e si aprirà un altra finiestra
    /// Quindi questa finestra è solo una finestra di "bellezza" (se vuoi la togliamo)
    /// </summary>
    public partial class MainWindow : Window
    {
        /// <summary>
        /// Represents the main window of the application.
        /// </summary>
        public MainWindow()
        {
            InitializeComponent();
        }
        /// <summary>
        /// Event handler for the button click event.
        /// Creates an instance of the second window and shows it while closing the current window.
        /// </summary>
        /// <param name="sender">The object that raised the event.</param>
        /// <param name="e">The event arguments.</param>
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            // Creazione di un'istanza della seconda finestra
            WindowPaginaDiLogin WindowLogin = new WindowPaginaDiLogin();

            // Mostra la nuova finestra
            WindowLogin.Show();
            //chiudi questa finestra
            this.Close();
        }
    }
}
