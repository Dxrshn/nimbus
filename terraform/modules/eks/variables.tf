variable "project" {
  type    = string
  default = "nimbus"
}

variable "env" {
  type    = string
  default = "dev"
}

variable "kubernetes_version" {
  type    = string
  default = "1.31"
}

variable "public_subnet_ids" {
  type    = list(string)
}

variable "private_subnet_ids" {
  type    = list(string)
}

variable "node_role_arn" {
  type    = string
}

variable "instance_types" {
  type    = list(string)
  default = ["t3.medium"]
}

variable "desired_size" {
  type    = number
  default = 2
}

variable "min_size" {
  type    = number
  default = 1
}

variable "max_size" {
  type    = number
  default = 4
}

variable "tags" {
  type    = map(string)
  default = {}
}
