using System.Data;
using SQL.API.Data;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace SQL.API
{
  public class Startup
  {
    public Startup(IConfiguration configuration)
    {
      Configuration = configuration;
    }

    public IConfiguration Configuration { get; }

    // This method gets called by the runtime. Use this method to add services to the container.
    public void ConfigureServices(IServiceCollection services)
    {
      // Read the connection string from appsettings.
      string dbConnectionString = this.Configuration.GetConnectionString("DefaultConnection");

      // Inject IDbConnection, with implementation from SqlConnection class.
      services.AddTransient<IDbConnection>((sp) => new SqlConnection(dbConnectionString));

      services.AddControllers();
      services.AddCors();
      services.AddScoped<ISqlRepository, SqlRepository>();
    }

    // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
      if (env.IsDevelopment())
      {
        app.UseDeveloperExceptionPage();
      }

      // app.UseHttpsRedirection();

      app.UseRouting();

      app.UseCors(x => x.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader());

      // app.UseAuthorization();

      app.UseEndpoints(endpoints =>
      {
        endpoints.MapControllers();
      });
    }
  }
}
