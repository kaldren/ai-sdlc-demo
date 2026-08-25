@description('Base name used to derive resource names (lowercase, alphanumeric + dashes).')
param appName string = 'tasktracker'

param location string = resourceGroup().location

@description('Postgres Flexible Server region. Kept separate from `location` because not every region allows new Postgres Flexible Server provisioning for every subscription type — a resource group can span regions, so this only needs to match wherever Postgres is actually available.')
param postgresLocation string = location

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
    location: postgresLocation
    administratorLogin: postgresAdminLogin
    administratorPassword: postgresAdminPassword
    databaseName: databaseName
  }
}

var backendAppName = '${appName}-backend'
var frontendFqdn = '${appName}-frontend.${containerAppsEnvironment.outputs.defaultDomain}'

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
      {
        name: 'PGHOST'
        value: postgres.outputs.fqdn
      }
      {
        name: 'PGPORT'
        value: '5432'
      }
      {
        name: 'PGUSER'
        value: postgresAdminLogin
      }
      {
        name: 'PGDATABASE'
        value: databaseName
      }
      {
        name: 'PGSSLMODE'
        value: 'require'
      }
    ]
    // Passed through unconcatenated so the secure password param never gets combined
    // with other values into a plain (non-secure) Bicep variable or expression.
    secretEnv: {
      PGPASSWORD: postgresAdminPassword
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
