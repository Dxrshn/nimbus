variable "project" {
  type    = string
  default = "nimbus"
}

variable "env" {
  type    = string
  default = "dev"
}

variable "tags" {
  type    = map(string)
  default = {}
}
