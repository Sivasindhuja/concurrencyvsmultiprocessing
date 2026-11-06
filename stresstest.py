"""Stress-test the five FastAPI endpoints with concurrent HTTP requests."""

import argparse
import asyncio
import math
import statistics
import time

import httpx

DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_REQUESTS = 20
DEFAULT_CONCURRENCY = 20
DEFAULT_TIMEOUT = 300.0

ENDPOINTS = [
    "/blocking-io",
    "/async-io",
    "/cpu-bound",
    "/cpu-process",
    "/cpu-process-trueparallelism",
]


async def send_request(client, url, semaphore):
    """Send one request; return (latency, error) without raising."""
    async with semaphore:
        started = time.perf_counter()
        try:
            response = await client.get(url)
            latency = time.perf_counter() - started
            if 200 <= response.status_code < 300:
                return latency, None
            return latency, f"HTTP {response.status_code}"
        except Exception as exc:  # Network errors, timeouts, etc.
            latency = time.perf_counter() - started
            return latency, f"{type(exc).__name__}: {exc}"


def percentile(values, pct):
    """Nearest-rank percentile for a small list of values."""
    if not values:
        return None
    ordered = sorted(values)
    rank = math.ceil(pct / 100.0 * len(ordered))
    return ordered[max(rank - 1, 0)]


async def run_endpoint(client, base_url, endpoint, requests, concurrency):
    url = base_url.rstrip("/") + endpoint
    semaphore = asyncio.Semaphore(concurrency)

    started = time.perf_counter()
    results = await asyncio.gather(
        *(send_request(client, url, semaphore) for _ in range(requests))
    )
    duration = time.perf_counter() - started

    latencies = [latency for latency, error in results if error is None]
    failures = [error for _, error in results if error is not None]

    return {
        "endpoint": endpoint,
        "duration": duration,
        "avg_ms": statistics.mean(latencies) * 1000 if latencies else None,
        "p95_ms": (
            percentile(latencies, 95) * 1000 if latencies else None
        ),
        "throughput": requests / duration if duration else 0.0,
        "failed": len(failures),
        "first_error": failures[0] if failures else None,
    }


def print_results(rows):
    print("\nFastAPI stress-test results")
    print(
        f"{'Endpoint':<32}{'Total (s)':>11}{'Avg (ms)':>11}"
        f"{'P95 (ms)':>11}{'Req/s':>10}{'Failed':>8}"
    )
    print("-" * 83)

    for row in rows:
        avg = "N/A" if row["avg_ms"] is None else f"{row['avg_ms']:.1f}"
        p95 = "N/A" if row["p95_ms"] is None else f"{row['p95_ms']:.1f}"
        print(
            f"{row['endpoint']:<32}{row['duration']:>11.2f}{avg:>11}"
            f"{p95:>11}{row['throughput']:>10.2f}{row['failed']:>8}"
        )

    failures = [row for row in rows if row["first_error"]]
    if failures:
        print("\nFirst error per endpoint:")
        for row in failures:
            print(f"  {row['endpoint']}: {row['first_error']}")


async def main():
    parser = argparse.ArgumentParser(
        description="Stress-test the FastAPI benchmark endpoints."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--requests", type=int, default=DEFAULT_REQUESTS)
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()

    print(
        f"Testing {args.requests} requests per endpoint with "
        f"concurrency {args.concurrency}"
    )

    rows = []
    async with httpx.AsyncClient(timeout=args.timeout) as client:
        for endpoint in ENDPOINTS:
            print(f"Running {endpoint} ...")
            row = await run_endpoint(
                client,
                args.base_url,
                endpoint,
                args.requests,
                args.concurrency,
            )
            rows.append(row)

    print_results(rows)


if __name__ == "__main__":
    asyncio.run(main())
