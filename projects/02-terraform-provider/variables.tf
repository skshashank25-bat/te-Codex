variable "te_token" {
  description = "ThousandEyes bearer token."
  type        = string
  sensitive   = true
}

variable "te_aid" {
  description = "ThousandEyes account group ID."
  type        = string
}

variable "te_api_endpoint" {
  description = "ThousandEyes API endpoint. Provider v3 supports API v7."
  type        = string
  default     = "https://api.thousandeyes.com/v7"
}

variable "agent_name" {
  description = "Cloud or Enterprise Agent name to use as the source."
  type        = string
  default     = "Melbourne, Australia"
}

variable "interval" {
  description = "Test interval in seconds."
  type        = number
  default     = 300
}

variable "enable_agent_to_server" {
  description = "Create the agent-to-server test when true."
  type        = bool
  default     = false
}

variable "enable_http_server" {
  description = "Create the HTTP server test when true."
  type        = bool
  default     = false
}

variable "enable_dns_server" {
  description = "Create the DNS server test when true."
  type        = bool
  default     = false
}

variable "agent_to_server_test_name" {
  description = "Name for the agent-to-server test."
  type        = string
  default     = "GitHub Playground - Agent to Server"
}

variable "http_server_test_name" {
  description = "Name for the HTTP server test."
  type        = string
  default     = "GitHub Playground - HTTP Server"
}

variable "dns_server_test_name" {
  description = "Name for the DNS server test."
  type        = string
  default     = "GitHub Playground - DNS Server"
}

variable "target_server" {
  description = "Hostname for the agent-to-server test."
  type        = string
  default     = "www.thousandeyes.com"
}

variable "target_port" {
  description = "Port for the agent-to-server test."
  type        = number
  default     = 443
}

variable "http_url" {
  description = "URL for the HTTP server test."
  type        = string
  default     = "https://www.thousandeyes.com"
}

variable "dns_domain" {
  description = "DNS record and type to resolve."
  type        = string
  default     = "www.thousandeyes.com ANY"
}

variable "dns_servers" {
  description = "DNS servers to query."
  type        = set(string)
  default     = ["ns1.google.com"]
}
