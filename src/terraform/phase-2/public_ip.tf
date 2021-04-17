resource "azurerm_public_ip" "public_ip_1" {
  name                = var.public_ip_name
  resource_group_name = azurerm_resource_group.rl_hypothesis_2_resource_group.name
  location            = azurerm_resource_group.rl_hypothesis_2_resource_group.location
  allocation_method   = "Static"
  domain_name_label   = var.public_domain_prefix
}

