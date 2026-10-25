# AI cost model

Track per workload and environment: model, region, billing meter, token/request mix, GPU hours, utilization, search, storage, networking, logging, latency and quality thresholds.

| Metric | Definition |
|---|---|
| Total platform cost | Allocated eligible Azure costs |
| Cost per 1,000 requests | Workload cost / requests × 1,000 |
| Cost per successful task | Workload cost / qualifying successes |
| Budget variance | Actual minus budget |
| Realized savings | Comparable normalized baseline minus actual |

Measure 7–30 days of representative workloads where feasible; record scope, demand, response quality and latency before/after each change.
