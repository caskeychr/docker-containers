# FROM microsoft/dotnet:sdk AS build-env
FROM mcr.microsoft.com/dotnet/core/sdk:3.1 AS build
WORKDIR /build
COPY . .
RUN dotnet restore
RUN dotnet publish -c Release -o /app

# Build runtime image
# FROM microsoft/dotnet:aspnetcore-runtime
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "SQL.API.dll"]

