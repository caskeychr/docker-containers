using System.ComponentModel.DataAnnotations;

namespace SQL.API.Dtos
{
  public class RequestDto
  {
    [Required]
    public string text { get; set; }
  }
}