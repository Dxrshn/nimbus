package publisher

import (
	"context"
	"encoding/json"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	awsconfig "github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/sqs"
)

type ClickEvent struct {
	ShortCode string    `json:"short_code"`
	ClickedAt time.Time `json:"clicked_at"`
	UserAgent string    `json:"user_agent"`
	Referrer  string    `json:"referrer"`
}

type SQS struct {
	client   *sqs.Client
	queueURL string
}

func NewSQS(endpoint, queueURL, region string) *SQS {
	cfg, _ := awsconfig.LoadDefaultConfig(context.Background(),
		awsconfig.WithRegion(region),
		awsconfig.WithBaseEndpoint(endpoint),
	)
	return &SQS{
		client:   sqs.NewFromConfig(cfg),
		queueURL: queueURL,
	}
}

func (s *SQS) Publish(ctx context.Context, event ClickEvent) {
	body, err := json.Marshal(event)
	if err != nil {
		return
	}
	s.client.SendMessage(ctx, &sqs.SendMessageInput{
		QueueUrl:    aws.String(s.queueURL),
		MessageBody: aws.String(string(body)),
	})
}
