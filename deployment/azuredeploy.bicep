@description('The name of the function app that you wish to create.')
param appName string = 'fnapp${uniqueString(resourceGroup().id)}'

@allowed([
  'Standard_LRS'
  'Standard_GRS'
  'Standard_RAGRS'
])
@description('Storage Account type')
param storageAccountType string = 'Standard_LRS'

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Location for Application Insights')
param appInsightsLocation string = resourceGroup().location

var functionAppName_var = appName
var hostingPlanName_var = appName
var applicationInsightsName_var = appName
var storageAccountName_var = '${uniqueString(resourceGroup().id)}azfunctions'

resource storageAccountName 'Microsoft.Storage/storageAccounts@2019-06-01' = {
  name: storageAccountName_var
  location: location
  sku: {
    name: storageAccountType
  }
  kind: 'Storage'
}

resource hostingPlanName 'Microsoft.Web/serverfarms@2020-06-01' = {
  name: hostingPlanName_var
  location: location
  kind: 'linux'
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  properties: {
    reserved: true
  }
}

resource functionAppName 'Microsoft.Web/sites@2020-06-01' = {
  name: functionAppName_var
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: hostingPlanName.id
    siteConfig: {
      use32BitWorkerProcess: false
      linuxFxVersion: 'Python|3.9'
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccountName_var};EndpointSuffix=${environment().suffixes.storage};AccountKey=${listKeys(storageAccountName.id, '2019-06-01').keys[0].value}'
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~3'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: reference(applicationInsightsName.id, '2020-02-02-preview').InstrumentationKey
        }
      ]
    }
    clientAffinityEnabled: false
  }
}

resource applicationInsightsName 'microsoft.insights/components@2020-02-02-preview' = {
  name: applicationInsightsName_var
  location: appInsightsLocation
  kind: 'web'
  tags: {
    'hidden-link:${resourceId('Microsoft.Web/sites', applicationInsightsName_var)}': 'Resource'
  }
  properties: {
    Application_Type: 'web'
    Request_Source: 'rest'
  }
}
