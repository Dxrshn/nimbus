package store

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"
)

type Postgres struct {
	pool *pgxpool.Pool
}

func NewPostgres(url string) (*Postgres, error) {
	pool, err := pgxpool.New(context.Background(), url)
	if err != nil {
		return nil, err
	}
	return &Postgres{pool: pool}, nil
}

func (p *Postgres) GetOriginalURL(ctx context.Context, shortCode string) (string, error) {
	var originalURL string
	err := p.pool.QueryRow(ctx,
		"SELECT original_url FROM urls WHERE short_code = $1",
		shortCode,
	).Scan(&originalURL)
	if err != nil {
		return "", err
	}
	return originalURL, nil
}

func (p *Postgres) IncrementClickCount(ctx context.Context, shortCode string) {
	p.pool.Exec(ctx,
		"UPDATE urls SET click_count = click_count + 1 WHERE short_code = $1",
		shortCode,
	)
}

func (p *Postgres) Close() {
	p.pool.Close()
}