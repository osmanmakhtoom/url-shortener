Here’s a polished version you can drop into your repo. It’s written in a **professional, reviewer-friendly tone** and highlights how the system works, how it scales, and what trade-offs we’ve made.

---

# SCALABILITY.md

This document explains the scalability and performance strategy of the URL shortener service.
The project is built on **FastAPI (async)**, **Postgres (SQLModel/asyncpg)**, **Redis (asyncio client)**, and **RabbitMQ (aio-pika)**.
The design goal is to keep redirect latency near-zero while reliably capturing analytics and supporting future growth.

---

## 🎯 High-Level Goals

* **Low-latency redirects**: every `GET /{short_code}` should respond in milliseconds.
* **Non-blocking logging**: redirect path never waits on heavy analytics writes.
* **Independent scaling**: web layer, counters, and log processing can scale separately.
* **Operational resilience**: graceful degradation, observability, and predictable failure modes.

---

## 1. Redirect Path (critical hot path)

* Lookup flow:

  1. Check Redis cache → `short:{code} → original_url`.
  2. If cache miss, read from Postgres and set Redis with TTL.
  3. Return `307` redirect to client.

* Counters and logging are **offloaded**:

  * Increment `visits:{code}` in Redis (fast atomic `INCR`).
  * Publish a small JSON log event to RabbitMQ (`{ short_code, ip, timestamp }`).

This ensures the redirect itself remains fast, regardless of DB or worker load.

---

## 2. Logging & Analytics (non-blocking)

* **RabbitMQ** is used as a durable queue for visit logs.
* Workers consume the `visits` queue, batch messages, and insert visit rows into Postgres.
* Redis counters are periodically flushed back to Postgres for persistent aggregation.

Advantages:

* Web requests don’t block on database writes.
* Queue provides durability, buffering, and back-pressure handling.
* Workers can be scaled independently (e.g., add more consumers for high traffic).

---

## 3. Visit Counting & Aggregation

* **Fast counters** in Redis: `INCR visits:{code}` per redirect.
* **Periodic flush worker** moves deltas into Postgres (`urls.visit_count`).
* **Detailed analytics**: workers insert batched visit records (`visits` table).

This reduces write amplification on Postgres while preserving detailed logs for analysis.

---

## 4. Queue & Worker Strategy

* **Queue configuration**:

  * Durable queues, persistent messages.
  * Per-consumer prefetch (`channel.set_qos`) to balance throughput and fairness.
  * Dead-letter queues (DLQ) to capture poison messages.

* **Worker behavior**:

  * Batch inserts (e.g., 200 messages or 2 seconds).
  * Idempotent writes (safe retries).
  * Backoff and retry on transient errors.

* **Scaling**:

  * Add workers if queue depth grows.
  * RabbitMQ absorbs spikes, so the app stays responsive.

---

## 5. Database Strategy

* Postgres stores authoritative short-code metadata.
* Unique constraints ensure no duplicate codes.
* Connection pooling (asyncpg) tuned for concurrency.
* Writes are batched by workers, not the web path.
* For analytics scale-out: read replicas for reporting queries.

---

## 6. Caching Strategy

* Redis serves as the primary lookup cache.
* TTLs prevent unbounded growth; hot links can be pinned.
* Negative caching (short TTL) reduces repeated DB hits for non-existent codes.
* Supports campaign “pre-warming” (populate cache before traffic spike).

---

## 7. Multi-Instance Deployment

* API is **stateless** → horizontally scalable behind a load balancer.
* Shared state lives in Postgres, Redis, and RabbitMQ.
* Workers run as separate processes (or containers), scaling independently.

---

## 8. Handling Campaign Spikes (thousands req/s)

* Redirect path remains fast (cache + async publish).
* Redis absorbs high QPS counter increments.
* RabbitMQ buffers log events; workers catch up asynchronously.
* If under pressure:

  * Prioritize redirects → analytics may lag but service remains usable.
  * Autoscale API pods and worker pods.
  * Scale Redis vertically (or to cluster mode) and Postgres with replicas.

---

## 9. Observability

* **Metrics**: latency, Redis ops, RabbitMQ queue depth, DB pool usage, worker lag.
* **Tracing**: OpenTelemetry spans for redirect path and worker processing.
* **Logging**: structured JSON logs for central ingestion (ELK/Datadog).
* **Alerts**: high queue depth, DB connection exhaustion, Redis memory pressure.

---

## 10. Security & Ops Hygiene

* Use TLS for DB/Redis/RabbitMQ connections.
* Secrets from a vault (not in env files).
* Principle of least privilege for DB roles.
* API rate limiting and edge protections (CDN/WAF).

---

## 11. Cost vs Complexity

* **Early stage**: 1 app, 1 worker, Postgres + Redis + RabbitMQ → simple & cheap.
* **Growth**: managed Postgres, Redis cluster, RabbitMQ HA, autoscaling app + workers.
* **At scale**: Kafka for logs, ClickHouse/BigQuery for analytics, sharded Postgres for metadata.

---

## 12. Summary for Reviewers

This project uses **async I/O, Redis, and RabbitMQ** to keep the hot path (redirects) extremely fast, while moving heavy work (logging, counters, analytics) into **background workers**.
It scales horizontally at the API and worker level, while Postgres, Redis, and RabbitMQ can be tuned and clustered as traffic grows.
The architecture is **resilient, observable, and cost-efficient** for both early stages and large campaigns.

---

✅ This strikes a balance: simple enough to run locally or in small deployments, but ready for production scale with minimal changes.

---
