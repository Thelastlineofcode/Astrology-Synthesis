#!/usr/bin/env python3
"""Performance validation and SLA testing for astrology API."""

import asyncio
import time
import json
import statistics
from dataclasses import dataclass
from typing import List, Tuple
import httpx

@dataclass
class PerformanceResult:
    endpoint: str
    method: str
    requests: int
    success_count: int
    error_count: int
    min_time: float
    max_time: float
    avg_time: float
    p95_time: float
    p99_time: float
    throughput: float

class PerformanceValidator:
    def __init__(self, base_url: str = "http://localhost:8000", warmup_requests: int = 10):
        self.base_url = base_url
        self.warmup_requests = warmup_requests
        self.sla_targets = {
            "p95": 0.5,  # 500ms
            "p99": 1.0,  # 1s
            "error_rate": 0.01,  # 1%
        }

    async def health_check(self) -> bool:
        """Verify API is running."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False

    async def warmup(self, endpoint: str, method: str = "GET", data: dict = None):
        """Run warmup requests to stabilize timing."""
        async with httpx.AsyncClient() as client:
            for _ in range(self.warmup_requests):
                try:
                    if method == "GET":
                        await client.get(endpoint)
                    elif method == "POST":
                        await client.post(endpoint, json=data)
                except Exception:
                    pass

    async def measure_endpoint(
        self,
        endpoint: str,
        method: str = "GET",
        data: dict = None,
        concurrent_requests: int = 50
    ) -> PerformanceResult:
        """Measure endpoint performance under load."""
        url = f"{self.base_url}{endpoint}"
        
        # Warmup
        await self.warmup(url, method, data)
        
        times = []
        errors = 0
        success = 0
        start_time = time.time()

        async def make_request():
            nonlocal errors, success
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    req_start = time.time()
                    if method == "GET":
                        response = await client.get(url)
                    elif method == "POST":
                        response = await client.post(url, json=data)
                    req_time = time.time() - req_start
                    
                    if response.status_code in [200, 201]:
                        times.append(req_time)
                        success += 1
                    else:
                        errors += 1
            except Exception:
                errors += 1

        # Run concurrent requests
        tasks = [make_request() for _ in range(concurrent_requests)]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        if not times:
            times = [0]
        
        sorted_times = sorted(times)
        p95_idx = int(len(sorted_times) * 0.95)
        p99_idx = int(len(sorted_times) * 0.99)
        
        return PerformanceResult(
            endpoint=endpoint,
            method=method,
            requests=concurrent_requests,
            success_count=success,
            error_count=errors,
            min_time=min(times),
            max_time=max(times),
            avg_time=statistics.mean(times),
            p95_time=sorted_times[p95_idx] if p95_idx < len(sorted_times) else max(times),
            p99_time=sorted_times[p99_idx] if p99_idx < len(sorted_times) else max(times),
            throughput=concurrent_requests / total_time,
        )

    async def run_validation_suite(self) -> bool:
        """Run complete performance validation."""
        print("\n🔍 Performance Validation Suite")
        print("=" * 60)
        
        # Check health
        is_healthy = await self.health_check()
        if not is_healthy:
            print("❌ API is not healthy. Aborting validation.")
            return False
        print("✅ API is healthy")
        
        # Test endpoints
        test_cases = [
            ("/health", "GET", None, 100),
            ("/api/v1/charts", "GET", None, 50),
        ]
        
        results: List[PerformanceResult] = []
        all_passed = True
        
        for endpoint, method, data, concurrency in test_cases:
            print(f"\n📊 Testing {method} {endpoint} ({concurrency} concurrent)...")
            result = await self.measure_endpoint(endpoint, method, data, concurrency)
            results.append(result)
            
            # Check SLA
            error_rate = result.error_count / result.requests if result.requests > 0 else 0
            p95_pass = result.p95_time <= self.sla_targets["p95"]
            p99_pass = result.p99_time <= self.sla_targets["p99"]
            error_pass = error_rate <= self.sla_targets["error_rate"]
            
            print(f"  P95: {result.p95_time*1000:.1f}ms ({result.sla_targets.get('p95', 0.5)*1000:.0f}ms) {'✅' if p95_pass else '❌'}")
            print(f"  P99: {result.p99_time*1000:.1f}ms ({self.sla_targets['p99']*1000:.0f}ms) {'✅' if p99_pass else '❌'}")
            print(f"  Avg: {result.avg_time*1000:.1f}ms")
            print(f"  Throughput: {result.throughput:.1f} req/s")
            print(f"  Error Rate: {error_rate*100:.2f}% {'✅' if error_pass else '❌'}")
            
            if not (p95_pass and p99_pass and error_pass):
                all_passed = False
        
        # Summary
        print("\n" + "=" * 60)
        if all_passed:
            print("✅ All SLA targets met!")
        else:
            print("❌ Some SLA targets not met - see above for details")
        
        # Write results
        with open("performance_results.json", "w") as f:
            json.dump([{
                "endpoint": r.endpoint,
                "method": r.method,
                "requests": r.requests,
                "success_count": r.success_count,
                "error_count": r.error_count,
                "min_time_ms": r.min_time * 1000,
                "max_time_ms": r.max_time * 1000,
                "avg_time_ms": r.avg_time * 1000,
                "p95_time_ms": r.p95_time * 1000,
                "p99_time_ms": r.p99_time * 1000,
                "throughput_req_per_sec": r.throughput,
            } for r in results], f, indent=2)
        
        return all_passed

async def main():
    validator = PerformanceValidator()
    success = await validator.run_validation_suite()
    exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
