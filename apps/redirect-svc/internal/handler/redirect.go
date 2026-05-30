package handler

import (
	"context"
	"log/slog"
	"net/http"
	"time"

	"github.com/dxrshn/nimbus/redirect-svc/internal/publisher"
)

type Storer interface {
	GetOriginalURL(ctx context.Context, shortCode string) (string, error)
	IncrementClickCount(ctx context.Context, shortCode string)
}

type Cacher interface {
	Get(ctx context.Context, shortCode string) (string, error)
	Set(ctx context.Context, shortCode, originalURL string)
	Ping(ctx context.Context) error
}

type Publisher interface {
	Publish(ctx context.Context, event publisher.ClickEvent)
}

type Handler struct {
	pg     Storer
	cache  Cacher
	pub    Publisher
	logger *slog.Logger
}

func New(pg Storer, cache Cacher, pub Publisher, logger *slog.Logger) *Handler {
	return &Handler{pg: pg, cache: cache, pub: pub, logger: logger}
}

func (h *Handler) Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", h.health)
	mux.HandleFunc("/ready", h.ready)
	mux.HandleFunc("/", h.redirect)
	return mux
}

func (h *Handler) redirect(w http.ResponseWriter, r *http.Request) {
	shortCode := r.URL.Path[1:]
	if shortCode == "" {
		http.NotFound(w, r)
		return
	}

	ctx := r.Context()

	originalURL, err := h.cache.Get(ctx, shortCode)
	if err != nil {
		originalURL, err = h.pg.GetOriginalURL(ctx, shortCode)
		if err != nil {
			http.NotFound(w, r)
			return
		}
		h.cache.Set(ctx, shortCode, originalURL)
	}

	go h.pub.Publish(context.Background(), publisher.ClickEvent{
		ShortCode: shortCode,
		ClickedAt: time.Now().UTC(),
		UserAgent: r.Header.Get("User-Agent"),
		Referrer:  r.Header.Get("Referer"),
	})

	go h.pg.IncrementClickCount(context.Background(), shortCode)

	http.Redirect(w, r, originalURL, http.StatusMovedPermanently)
}

func (h *Handler) health(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"status":"ok"}`))
}

func (h *Handler) ready(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	w.Header().Set("Content-Type", "application/json")
	if err := h.cache.Ping(ctx); err != nil {
		w.WriteHeader(http.StatusServiceUnavailable)
		w.Write([]byte(`{"status":"error","checks":{"redis":"error"}}`))
		return
	}
	w.Write([]byte(`{"status":"ok","checks":{"redis":"ok"}}`))
}