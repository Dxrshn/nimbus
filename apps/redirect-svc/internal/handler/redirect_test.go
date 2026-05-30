package handler

import (
	"context"
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/dxrshn/nimbus/redirect-svc/internal/publisher"
	"log/slog"
	"os"
)

type mockStore struct {
	url string
	err error
}

func (m *mockStore) GetOriginalURL(_ context.Context, _ string) (string, error) {
	return m.url, m.err
}
func (m *mockStore) IncrementClickCount(_ context.Context, _ string) {}

type mockCache struct {
	url    string
	getErr error
	pinged bool
}

func (m *mockCache) Get(_ context.Context, _ string) (string, error) {
	return m.url, m.getErr
}
func (m *mockCache) Set(_ context.Context, _, _ string) {}
func (m *mockCache) Ping(_ context.Context) error {
	if m.pinged {
		return nil
	}
	return errors.New("redis down")
}

type mockPublisher struct{}

func (m *mockPublisher) Publish(_ context.Context, _ publisher.ClickEvent) {}

func newTestHandler(pg Storer, cache Cacher, pub Publisher) *Handler {
	logger := slog.New(slog.NewTextHandler(os.Stdout, nil))
	return New(pg, cache, pub, logger)
}

func TestRedirect_CacheHit(t *testing.T) {
	h := newTestHandler(
		&mockStore{},
		&mockCache{url: "https://github.com"},
		&mockPublisher{},
	)

	req := httptest.NewRequest(http.MethodGet, "/abc123", nil)
	rr := httptest.NewRecorder()
	h.redirect(rr, req)

	if rr.Code != http.StatusMovedPermanently {
		t.Fatalf("expected 301, got %d", rr.Code)
	}
	if rr.Header().Get("Location") != "https://github.com" {
		t.Fatalf("unexpected location: %s", rr.Header().Get("Location"))
	}
}

func TestRedirect_CacheMiss_DBHit(t *testing.T) {
	h := newTestHandler(
		&mockStore{url: "https://example.com"},
		&mockCache{getErr: errors.New("miss")},
		&mockPublisher{},
	)

	req := httptest.NewRequest(http.MethodGet, "/xyz", nil)
	rr := httptest.NewRecorder()
	h.redirect(rr, req)

	if rr.Code != http.StatusMovedPermanently {
		t.Fatalf("expected 301, got %d", rr.Code)
	}
}

func TestRedirect_NotFound(t *testing.T) {
	h := newTestHandler(
		&mockStore{err: errors.New("not found")},
		&mockCache{getErr: errors.New("miss")},
		&mockPublisher{},
	)

	req := httptest.NewRequest(http.MethodGet, "/gone", nil)
	rr := httptest.NewRecorder()
	h.redirect(rr, req)

	if rr.Code != http.StatusNotFound {
		t.Fatalf("expected 404, got %d", rr.Code)
	}
}

func TestRedirect_EmptyShortCode(t *testing.T) {
	h := newTestHandler(&mockStore{}, &mockCache{}, &mockPublisher{})

	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rr := httptest.NewRecorder()
	h.redirect(rr, req)

	if rr.Code != http.StatusNotFound {
		t.Fatalf("expected 404, got %d", rr.Code)
	}
}

func TestHealth(t *testing.T) {
	h := newTestHandler(&mockStore{}, &mockCache{}, &mockPublisher{})

	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rr := httptest.NewRecorder()
	h.health(rr, req)

	if rr.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rr.Code)
	}
}

func TestReady_Up(t *testing.T) {
	h := newTestHandler(&mockStore{}, &mockCache{pinged: true}, &mockPublisher{})

	req := httptest.NewRequest(http.MethodGet, "/ready", nil)
	rr := httptest.NewRecorder()
	h.ready(rr, req)

	if rr.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rr.Code)
	}
}

func TestReady_Down(t *testing.T) {
	h := newTestHandler(&mockStore{}, &mockCache{pinged: false}, &mockPublisher{})

	req := httptest.NewRequest(http.MethodGet, "/ready", nil)
	rr := httptest.NewRecorder()
	h.ready(rr, req)

	if rr.Code != http.StatusServiceUnavailable {
		t.Fatalf("expected 503, got %d", rr.Code)
	}
}
