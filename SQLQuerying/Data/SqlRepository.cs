using System.Collections.Generic;
using System.Data;
using System.Threading.Tasks;
using Dapper;
using Newtonsoft.Json;

namespace SQL.API.Data
{
  public class SqlRepository : ISqlRepository
  {
    private readonly IDbConnection _connection;

    public SqlRepository(IDbConnection connection)
    {
      _connection = connection;
    }

    public async Task<string> QueryNoResponse(string query)
    {
      System.Console.WriteLine(query);

      var queryOutput = await _connection.ExecuteAsync(query, commandTimeout: 0);

      var queryOutputString = queryOutput.ToString();

      var stringOutput = $@"{{ 
              ""rowsAffected"": {queryOutputString}
            }}";

      return stringOutput;
    }

    public async Task<string> QueryMultiple(string query)
    {
      System.Console.WriteLine(query);

      List<dynamic> allResults = new List<dynamic>();   //allResults is a generic list of dynamic objects containing result sets for each T-SQL query passed to Dapper Query Multiple.

      using (var results = await _connection.QueryMultipleAsync(query, commandTimeout: 0))
      {
        List<dynamic> list = new List<dynamic>();   //list is a generic list of dynamic objects containing a single result set for the T-SQL query we are currently reading.

        while (!results.IsConsumed)
        {       //do while there are result sets to read
          list = results.Read().AsList();   //get the result set for the current query    
          allResults.Add(list);             //add this result set to the allResults object, which (when finished reading result sets for each query, will contain all result sets.
        }

        //convert all result sets to a JSON string
        var jsonOutput = JsonConvert.SerializeObject(allResults);   //after all result sets are read for eadh T-SQL query passed to QueryMultiple(), convert to JSON.
        System.Console.WriteLine(jsonOutput);
        return jsonOutput;    //return all result sets in JSON format.
      }
    }
  }
}