variable "project" {
  type    = string
  default = "nimbus"
}

variable "env" {
  type    = string
  default = "dev"
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "database_url" {
  type      = string
  sensitive = true
}

variable "redis_url" {
  type      = string
  sensitive = true
}

variable "sqs_queue_url" {
  type    = string
}

variable "tags" {
  type    = map(string)
  default = {}
}
