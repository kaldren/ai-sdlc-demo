param name string
param location string
param environmentId string
param registryLoginServer string
param pullIdentityId string
param image string
param targetPort int
@description('Environment variables as {name, value} objects (non-secret).')
param env array = []
@description('Secret env vars as a {ENV_VAR_NAME: value} map; each entry is stored as a Container Apps secret and referenced via secretRef.')
@secure()
param secretEnv object = {}
param cpu string = '0.25'
param memory string = '0.5Gi'
param minReplicas int = 1
param maxReplicas int = 2

var secretEnvNames = items(secretEnv)

var secrets = [for e in secretEnvNames: {
  name: toLower(replace(e.key, '_', '-'))
  value: e.value
}]

var secretEnvVars = [for e in secretEnvNames: {
  name: e.key
  secretRef: toLower(replace(e.key, '_', '-'))
}]

resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: name
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${pullIdentityId}': {}
    }
  }
  properties: {
    managedEnvironmentId: environmentId
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: targetPort
        transport: 'auto'
      }
      registries: [
        {
          server: registryLoginServer
          identity: pullIdentityId
        }
      ]
      secrets: secrets
    }
    template: {
      containers: [
        {
          name: name
          image: image
          resources: {
            cpu: json(cpu)
            memory: memory
          }
          env: concat(env, secretEnvVars)
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
      }
    }
  }
}

output fqdn string = containerApp.properties.configuration.ingress.fqdn
output name string = containerApp.name
