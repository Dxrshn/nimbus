output "karpenter_controller_role_arn" {
  value = aws_iam_role.karpenter_controller.arn
}

output "node_role_arn" {
  value = aws_iam_role.node.arn
}

output "external_secrets_role_arn" {
  value = aws_iam_role.external_secrets.arn
}
