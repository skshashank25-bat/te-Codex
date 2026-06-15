terraform {
  required_version = ">= 1.5.0"

  required_providers {
    thousandeyes = {
      source  = "thousandeyes/thousandeyes"
      version = ">= 3.0.0"
    }
  }
}

provider "thousandeyes" {
  token            = var.te_token
  account_group_id = var.te_aid
  api_endpoint     = var.te_api_endpoint
}

data "thousandeyes_agent" "source" {
  agent_name = var.agent_name
}

resource "thousandeyes_agent_to_server" "playground" {
  count = var.enable_agent_to_server ? 1 : 0

  test_name            = var.agent_to_server_test_name
  interval             = var.interval
  alerts_enabled       = false
  server               = var.target_server
  port                 = var.target_port
  protocol             = "tcp"
  network_measurements = true
  agents               = [data.thousandeyes_agent.source.agent_id]
}

resource "thousandeyes_http_server" "playground" {
  count = var.enable_http_server ? 1 : 0

  test_name      = var.http_server_test_name
  interval       = var.interval
  alerts_enabled = false
  url            = var.http_url
  agents         = [data.thousandeyes_agent.source.agent_id]
}

resource "thousandeyes_dns_server" "playground" {
  count = var.enable_dns_server ? 1 : 0

  test_name      = var.dns_server_test_name
  interval       = var.interval
  alerts_enabled = false
  domain         = var.dns_domain
  dns_servers    = var.dns_servers
  agents         = [data.thousandeyes_agent.source.agent_id]
}
