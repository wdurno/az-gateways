provider "azurerm" {
  version = "=2.14.0"
  features {}
  
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}
