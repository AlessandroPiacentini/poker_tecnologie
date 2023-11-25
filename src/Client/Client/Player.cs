using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Client
{
    internal class Player
    {
        public string name;
        public int carta1;
        public int carta2;
        public float puntata;
        public int soldi;
        public string turno;
        public string blind;
        public bool seduto;
        public int posto;
        public int port;
        public string ip;

        public Player(string name, int carta1, int carta2, float puntata, int soldi, string turno, string blind, bool seduto, int posto)
        {
            this.name = name;
            this.carta1 = carta1;
            this.carta2 = carta2;
            this.puntata = puntata;
            this.soldi = soldi;
            this.turno = turno;
            this.blind = blind;
            this.seduto = seduto;
            this.posto = posto;
        }
    }
}
