# DLQ Replay Procedure

## Purpose

Replay messages from `fraud_detection.v1.dlq` once schema or processing issues are fixed.

## Preconditions

1. Root cause documented and fix deployed.
2. Consumer payload contract checks are green.
3. Replay window and message volume approved.

## Steps

1. Pause primary fraud consumer deployment.
2. Start a dedicated replay consumer group.
3. Read DLQ messages in bounded batches.
4. Re-validate message contract before re-publish.
5. Publish valid events to `fraud_detection.v1.retry`.
6. Keep irrecoverable records in DLQ and tag incident id.

## Post-Replay Validation

1. Confirm retry topic drains to near-zero.
2. Confirm no growth trend in DLQ after replay.
3. Confirm dbt freshness and quality checks return to green.
