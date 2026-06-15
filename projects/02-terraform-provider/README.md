# ThousandEyes Terraform Provider Starter

This starter uses the official `thousandeyes/thousandeyes` Terraform provider. It includes three small examples:

- `thousandeyes_agent_to_server`
- `thousandeyes_http_server`
- `thousandeyes_dns_server`

The examples are disabled by default through variables so you can run `terraform plan` intentionally before creating anything.

## Setup

Create a local tfvars file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Fill in `te_token`, `te_aid`, and the agent name you want to use.

## Commands

```bash
terraform init
terraform fmt -recursive
terraform validate
terraform plan
```

Enable one or more resources by setting these to `true` in `terraform.tfvars`:

```hcl
enable_agent_to_server = true
enable_http_server     = true
enable_dns_server      = true
```

## Safety

- `terraform.tfvars` is ignored by Git.
- Keep `enable_*` variables set to `false` until you are ready to create tests.
- Run `terraform plan` and review the resources before `terraform apply`.
