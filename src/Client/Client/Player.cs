using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Client
{
    /// <summary>
    /// Represents a player in the poker game.
    /// </summary>
    internal class Player
    {
        /// <summary>
        /// Gets or sets the name of the player.
        /// </summary>
        public string name;

        /// <summary>
        /// Gets or sets the value of the first card.
        /// </summary>
        public int carta1;

        /// <summary>
        /// Gets or sets the value of the second card.
        /// </summary>
        public int carta2;

        /// <summary>
        /// Gets or sets the amount of the bet.
        /// </summary>
        public float puntata;

        /// <summary>
        /// Gets or sets the amount of money the player has.
        /// </summary>
        public int soldi;

        /// <summary>
        /// Gets or sets the player's turn.
        /// </summary>
        public string turno;

        /// <summary>
        /// Gets or sets the player's blind.
        /// </summary>
        public string blind;

        /// <summary>
        /// Gets or sets a value indicating whether the player is seated.
        /// </summary>
        public bool seduto;

        /// <summary>
        /// Gets or sets the player's position.
        /// </summary>
        public int posto;

        /// <summary>
        /// Gets or sets the port number.
        /// </summary>
        public int port;

        /// <summary>
        /// Gets or sets the IP address.
        /// </summary>
        public string ip;

        /// <summary>
        /// Initializes a new instance of the <see cref="Player"/> class.
        /// </summary>
        /// <param name="name">The name of the player.</param>
        /// <param name="carta1">The value of the first card.</param>
        /// <param name="carta2">The value of the second card.</param>
        /// <param name="puntata">The amount of the bet.</param>
        /// <param name="soldi">The amount of money the player has.</param>
        /// <param name="turno">The player's turn.</param>
        /// <param name="blind">The player's blind.</param>
        /// <param name="seduto">A value indicating whether the player is seated.</param>
        /// <param name="posto">The player's position.</param>
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
