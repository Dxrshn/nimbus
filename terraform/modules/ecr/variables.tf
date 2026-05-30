variable "project" {
  type    = string
  default = "nimbus"
}

variable "repository_names" {
  type    = list(string)
  default = ["shortener-api", "redirect-svc", "analytics-worker", "dashboard-ui"]
}

variable "tags" {
  type    = map(string)
  default = {}
}
