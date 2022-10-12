using System;
using System.Threading.Tasks;
using SQL.API.Data;
using SQL.API.Dtos;
using Microsoft.AspNetCore.Mvc;

namespace SQL.API.Controllers
{
  [Route("api/[controller]")]
  [ApiController]

  public class SQLController : ControllerBase
  {
    public ISqlRepository _repo { get; }

    public SQLController(ISqlRepository repo)
    {
      _repo = repo;
    }

    [HttpPost("sqlQueryNoResponse")]
    public async Task<IActionResult> sqlQueryNoResponse(RequestDto requestDto)
    {
      try
      {
        var result = await _repo.QueryNoResponse(requestDto.text);

        return Ok(result);
      }
      catch (Exception e)
      {
        System.Console.WriteLine(e.Message);
        return StatusCode(500, e.Message);
      }

    }

    [HttpPost("sqlQuery")]
    public async Task<IActionResult> sqlQuery(RequestDto requestDto)
    {
      try
      {
        var result = await _repo.QueryMultiple(requestDto.text);

        return Ok(result);
      }
      catch (Exception e)
      {
        System.Console.WriteLine(e.Message);
        return StatusCode(500, e.Message);
      }
    }
  }
}