@description('Base name used to derive resource names (lowercase, alphanumeric + dashes).')
param appName string = 'tasktracker'

param location string = resourceGroup().location

param postgresAdminLogin string = 'taskadmin'

@secure()
param postgresAdminPassword string

@description('Backend image reference. Left as a placeholder on first deploy; CI updates it afterwards.')
param backendImage string = 'mcr.microsoft.com/k8se/quickstart:latest'

@description('Frontend image reference. Left as a placeholder on first deploy; CI updates it afterwards.')
param frontendImage string = 'mcr.microsoft.com/k8se/quickstart:latest'

var uniqueSuffix = uniqueString(resourceGroup().id)
var acrName = toLower('${replace(appName, '-', '')}acr${uniqueSuffix}')
var postgresServerName = toLower('${appName}-pg-${uniqueSuffix}')
var databaseName = 'tasktracker'

module containerRegistry 'modules/container-registry.bicep' = {
  name: 'containerRegistry'
  params: {
    name: acrName
    location: location
  }
}

module containerAppsEnvironment 'modules/container-apps-environment.bicep' = {
  name: 'containerAppsEnvironment'
  params: {
    name: '${appName}-env'
    location: location
    logAnalyticsName: '${appName}-logs'
  }
}

module postgres 'modules/postgres.bicep' = {
  name: 'postgres'
  params: {
    serverName: postgresServerName
    location: location
    administratorLogin: postgresAdminLogin
    administratorPassword: postgresAdminPassword
    databaseName: databaseName
  }
}

var backendAppName = '${appName}-backend'
var frontendFqdn = '${appName}-frontend.${containerAppsEnvironment.outputs.defaultDomain}'
var databaseUrl = 'postgresql+psycopg://${postgresAdminLogin}:${postgresAdminPassword}@${postgres.outputs.fqdn}:5432/${databaseName}?sslmode=require'

module backendApp 'modules/container-app.bicep' = {
  name: 'backendApp'
  params: {
    name: backendAppName
    location: location
    environmentId: containerAppsEnvironment.outputs.id
    registryLoginServer: containerRegistry.outputs.loginServer
    pullIdentityId: containerRegistry.outputs.pullIdentityId
    image: backendImage
    targetPort: 8000
    env: [
      {
        name: 'CORS_ORIGINS'
        value: 'https://${frontendFqdn}'
      }
    ]
    secretEnv: {
      DATABASE_URL: databaseUrl
    }
  }
}

module frontendApp 'modules/container-app.bicep' = {
  name: 'frontendApp'
  params: {
    name: '${appName}-frontend'
    location: location
    environmentId: containerAppsEnvironment.outputs.id
    registryLoginServer: containerRegistry.outputs.loginServer
    pullIdentityId: containerRegistry.outputs.pullIdentityId
    image: frontendImage
    targetPort: 80
    env: [
      {
        name: 'API_BASE_URL'
        value: 'https://${backendApp.outputs.fqdn}'
      }
    ]
  }
}

output acrName string = containerRegistry.outputs.name
output acrLoginServer string = containerRegistry.outputs.loginServer
output backendAppName string = backendApp.outputs.name
output frontendAppName string = frontendApp.outputs.name
output backendFqdn string = backendApp.outputs.fqdn
output frontendFqdn string = frontendApp.outputs.fqdn
