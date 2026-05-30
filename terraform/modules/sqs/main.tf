terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_sqs_queue" "click_events_dlq" {
  name                      = "${var.project}-${var.env}-click-events-dlq"
  message_retention_seconds = 1209600
  tags                      = var.tags
}

resource "aws_sqs_queue" "click_events" {
  name                       = "${var.project}-${var.env}-click-events"
  visibility_timeout_seconds = 30
  message_retention_seconds  = 86400

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.click_events_dlq.arn
    maxReceiveCount     = 3
  })

  tags = var.tags
}
