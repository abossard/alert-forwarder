param subscriptionId string
param name string
param location string
param hostingPlanName string
param serverFarmResourceGroup string
param alwaysOn bool
param storageAccountName string
param use32BitWorkerProcess bool
param linuxFxVersion string
param sku string
param skuCode string
param workerSize string
param workerSizeId string
param numberOfWorkers string

resource name_resource 'Microsoft.Web/sites@2018-11-01' = {
  name: name
  kind: 'functionapp,linux'
  location: location
  tags: {}
  properties: {
    name: name
    siteConfig: {
      appSettings: [
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
          value: reference('microsoft.insights/components/sadasdasdasd', '2015-05-01').InstrumentationKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: reference('microsoft.insights/components/sadasdasdasd', '2015-05-01').ConnectionString
        }
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccountName};AccountKey=${listKeys(storageAccountName_resource.id, '2019-06-01').keys[0].value};EndpointSuffix=core.windows.net'
        }
      ]
      use32BitWorkerProcess: use32BitWorkerProcess
      linuxFxVersion: linuxFxVersion
    }
    serverFarmId: '/subscriptions/${subscriptionId}/resourcegroups/${serverFarmResourceGroup}/providers/Microsoft.Web/serverfarms/${hostingPlanName}'
    clientAffinityEnabled: false
  }
  dependsOn: [
    sadasdasdasd
    hostingPlanName_resource
  ]
}

resource hostingPlanName_resource 'Microsoft.Web/serverfarms@2018-11-01' = {
  name: hostingPlanName
  location: location
  kind: 'linux'
  tags: {}
  properties: {
    name: hostingPlanName
    workerSize: workerSize
    workerSizeId: workerSizeId
    numberOfWorkers: numberOfWorkers
    reserved: true
  }
  sku: {
    Tier: sku
    Name: skuCode
  }
  dependsOn: []
}

resource sadasdasdasd 'microsoft.insights/components@2020-02-02-preview' = {
  name: 'sadasdasdasd'
  location: 'westeurope'
  tags: {}
  properties: {
    ApplicationId: name
    Request_Source: 'IbizaWebAppExtensionCreate'
    Flow_Type: 'Redfield'
    Application_Type: 'web'
    WorkspaceResourceId: '/subscriptions/8b25cfae-660b-4066-9ce5-0858e9ab3eac/resourcegroups/defaultresourcegroup-weu/providers/microsoft.operationalinsights/workspaces/defaultworkspace-8b25cfae-660b-4066-9ce5-0858e9ab3eac-weu'
  }
  dependsOn: []
}

resource storageAccountName_resource 'Microsoft.Storage/storageAccounts@2019-06-01' = {
  name: storageAccountName
  location: location
  tags: {}
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
  }
}