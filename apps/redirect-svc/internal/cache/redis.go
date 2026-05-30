package cache

import (
	"context"
	"time"

	"github.com/redis/go-redis/v9"
)

type Redis struct {
	client *redis.Client
}

func NewRedis(url string) *Redis {
	opts, _ := redis.ParseURL(url)
	return &Redis{client: redis.NewClient(opts)}
}

func (r *Redis) Get(ctx context.Context, shortCode string) (string, error) {
	return r.client.Get(ctx, "url:"+shortCode).Result()
}

func (r *Redis) Set(ctx context.Context, shortCode, originalURL string) {
	r.client.Set(ctx, "url:"+shortCode, originalURL, time.Hour)
}

func (r *Redis) Ping(ctx context.Context) error {
	return r.client.Ping(ctx).Err()
}

func (r *Redis) Close() {
	r.client.Close()
}