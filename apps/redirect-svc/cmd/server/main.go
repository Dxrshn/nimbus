package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/dxrshn/nimbus/redirect-svc/internal/handler"
	"github.com/dxrshn/nimbus/redirect-svc/internal/cache"
	"github.com/dxrshn/nimbus/redirect-svc/internal/store"
	"github.com/dxrshn/nimbus/redirect-svc/internal/publisher"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

	pg, err := store.NewPostgres(getenv("DATABASE_URL", "postgres://nimbus:nimbus-local-dev@localhost:5432/nimbus?sslmode=disable"))
	if err != nil {
		logger.Error("postgres connect failed", "err", err)
		os.Exit(1)
	}
	defer pg.Close()

	rdb := cache.NewRedis(getenv("REDIS_URL", "redis://localhost:6379"))
	defer rdb.Close()

	pub := publisher.NewSQS(
		getenv("SQS_ENDPOINT", "http://localhost:4566"),
		getenv("SQS_QUEUE_URL", "http://localhost:4566/000000000000/click-events"),
		getenv("AWS_DEFAULT_REGION", "ap-south-1"),
	)

	h := handler.New(pg, rdb, pub, logger)

	srv := &http.Server{
		Addr:         ":" + getenv("PORT", "8080"),
		Handler:      h.Routes(),
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	go func() {
		logger.Info("starting redirect-svc", "port", getenv("PORT", "8080"))
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Error("server error", "err", err)
			os.Exit(1)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	srv.Shutdown(ctx)
}

func getenv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}