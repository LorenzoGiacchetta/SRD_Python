using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace DDR.Models
{
    public class Patente
    {
        public int PatenteId { get; set; }
        [Required, StringLength(9)]
        public string Caracteres { get; set; }
        public bool Pagada { get; set; }
    }
}
