output "agent_id" {
  description = "Resolved source agent ID."
  value       = data.thousandeyes_agent.source.agent_id
}

output "agent_to_server_test_id" {
  description = "Created agent-to-server test ID, when enabled."
  value       = try(thousandeyes_agent_to_server.playground[0].test_id, null)
}

output "http_server_test_id" {
  description = "Created HTTP server test ID, when enabled."
  value       = try(thousandeyes_http_server.playground[0].test_id, null)
}

output "dns_server_test_id" {
  description = "Created DNS server test ID, when enabled."
  value       = try(thousandeyes_dns_server.playground[0].test_id, null)
}
