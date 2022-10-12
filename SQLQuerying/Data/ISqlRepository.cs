using System.Threading.Tasks;

namespace SQL.API.Data
{
  public interface ISqlRepository
  {
    Task<string> QueryNoResponse(string query);
    Task<string> QueryMultiple(string query);
  }
}