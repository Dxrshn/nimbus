variable "project" {
  type    = string
  default = "nimbus"
}

variable "env" {
  type    = string
  default = "dev"
}

variable "cluster_oidc_issuer_url" {
  type        = string
  description = "OIDC issuer URL from the EKS cluster"
}

variable "cluster_oidc_thumbprint" {
  type        = string
  description = "Thumbprint of the OIDC issuer certificate"
  default     = "9e99a48a9960b14926bb7f3b02e22da2b0ab7280"
}

variable "tags" {
  type    = map(string)
  default = {}
}
