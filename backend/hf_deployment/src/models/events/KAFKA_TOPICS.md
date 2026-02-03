# Kafka Topics for Todo Evolution

This document describes the Kafka topics used in the Todo Evolution application for event-driven architecture.

## Topic Configuration

All topics are configured with the following defaults:
- **Partitions**: 3
- **Replication Factor**: 3 (production), 1 (development)
- **Retention**: 7 days (168 hours)
- **Compression**: Snappy
- **Min In-Sync Replicas**: 2 (production), 1 (development)

## Topics

### 1. task.created

**Purpose**: Published when a new task is created

**Schema**:
```json
{
  "event_id": "uuid",
  "event_type": "task.created",
  "timestamp": "ISO 8601 datetime",
  "user_id": "string (optional)",
  "task_id": "string",
  "title": "string",
  "description": "string (optional)",
  "priority": "string (optional): low|medium|high",
  "due_date": "ISO 8601 datetime (optional)",
  "tags": ["string"],
  "source": "string",
  "version": "string"
}
```

**Consumers**:
- Analytics service (for task creation metrics)
- Notification service (for user notifications)
- Search indexer (for full-text search)
- Audit log service

**Throughput**: ~100 events/sec (expected)

---

### 2. task.updated

**Purpose**: Published when a task is modified

**Schema**:
```json
{
  "event_id": "uuid",
  "event_type": "task.updated",
  "timestamp": "ISO 8601 datetime",
  "user_id": "string (optional)",
  "task_id": "string",
  "changes": {
    "field_name": "new_value"
  },
  "previous_values": {
    "field_name": "old_value"
  },
  "source": "string",
  "version": "string"
}
```

**Consumers**:
- Analytics service (for update frequency metrics)
- Search indexer (for re-indexing)
- Change log service
- Notification service (for collaborators)

**Throughput**: ~200 events/sec (expected)

---

### 3. task.deleted

**Purpose**: Published when a task is deleted (soft or hard delete)

**Schema**:
```json
{
  "event_id": "uuid",
  "event_type": "task.deleted",
  "timestamp": "ISO 8601 datetime",
  "user_id": "string (optional)",
  "task_id": "string",
  "task_title": "string",
  "soft_delete": "boolean",
  "source": "string",
  "version": "string"
}
```

**Consumers**:
- Archive service (for soft deletes)
- Cleanup service (for hard deletes)
- Search indexer (for removing from index)
- Analytics service (for deletion metrics)

**Throughput**: ~50 events/sec (expected)

---

### 4. task.completed

**Purpose**: Published when a task is marked as completed

**Schema**:
```json
{
  "event_id": "uuid",
  "event_type": "task.completed",
  "timestamp": "ISO 8601 datetime",
  "user_id": "string (optional)",
  "task_id": "string",
  "task_title": "string",
  "completed_at": "ISO 8601 datetime",
  "time_to_complete": "integer (seconds, optional)",
  "source": "string",
  "version": "string"
}
```

**Consumers**:
- Analytics service (for completion metrics)
- Gamification service (for achievements/badges)
- Notification service (for congratulations)
- Productivity insights service

**Throughput**: ~150 events/sec (expected)

---

## Event Guarantees

### At-Least-Once Delivery

All events are guaranteed to be delivered at least once. Consumers must be idempotent to handle duplicate events.

**Idempotency Key**: Use `event_id` as the idempotency key to deduplicate events.

### Ordering

Events for the same `task_id` are guaranteed to be ordered within a partition when using `task_id` as the partition key.

### Retention

Events are retained for 7 days by default. For long-term analytics, events should be stored in a data warehouse.

## Consumer Groups

### Primary Consumer Group
- **Group ID**: `todo-app-consumer-group`
- **Purpose**: Main application event processing
- **Lag Tolerance**: < 1 second

### Analytics Consumer Group
- **Group ID**: `todo-app-analytics-group`
- **Purpose**: Real-time analytics and metrics
- **Lag Tolerance**: < 5 seconds

### Backup Consumer Group
- **Group ID**: `todo-app-backup-group`
- **Purpose**: Event backup to S3/GCS
- **Lag Tolerance**: < 1 hour

## Monitoring

### Key Metrics to Monitor

1. **Producer Metrics**:
   - `kafka_producer_record_send_rate`: Events published per second
   - `kafka_producer_record_error_rate`: Failed publish rate
   - `kafka_producer_request_latency_avg`: Average publish latency

2. **Consumer Metrics**:
   - `kafka_consumer_records_consumed_rate`: Events consumed per second
   - `kafka_consumer_lag`: Consumer lag per partition
   - `kafka_consumer_commit_latency_avg`: Commit latency

3. **Topic Metrics**:
   - `kafka_topic_partitions`: Number of partitions
   - `kafka_topic_size_bytes`: Topic size in bytes
   - `kafka_topic_messages_in_per_sec`: Incoming message rate

### Alerts

- **High Consumer Lag**: Alert if lag > 1000 messages for > 5 minutes
- **High Error Rate**: Alert if error rate > 1% for > 2 minutes
- **Low Throughput**: Alert if throughput drops > 50% for > 5 minutes

## Troubleshooting

### Common Issues

1. **Consumer Lag Increasing**:
   - Scale up consumer instances
   - Increase partition count
   - Optimize consumer processing logic

2. **Failed Event Publishing**:
   - Check Kafka broker health
   - Verify network connectivity
   - Review producer logs for errors

3. **Duplicate Events**:
   - Ensure consumers implement idempotency
   - Check for network issues causing retries
   - Verify consumer offset commits

## Testing

### Local Testing

```bash
# List topics
kafka-topics.sh --bootstrap-server localhost:9092 --list

# Describe topic
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic task.created

# Consume from beginning
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic task.created --from-beginning

# Produce test event
echo '{"event_id":"test-123","event_type":"task.created","task_id":"task-456","title":"Test Task"}' | \
  kafka-console-producer.sh --bootstrap-server localhost:9092 --topic task.created
```

### Load Testing

Use `kafka-producer-perf-test` and `kafka-consumer-perf-test` for load testing:

```bash
# Producer performance test
kafka-producer-perf-test.sh --topic task.created \
  --num-records 10000 \
  --record-size 1024 \
  --throughput 1000 \
  --producer-props bootstrap.servers=localhost:9092

# Consumer performance test
kafka-consumer-perf-test.sh --bootstrap-server localhost:9092 \
  --topic task.created \
  --messages 10000 \
  --group test-consumer-group
```

## Schema Evolution

When evolving event schemas:

1. **Backward Compatible**: Add optional fields only
2. **Version Field**: Always include `version` field in events
3. **Deprecated Fields**: Mark as deprecated, don't remove immediately
4. **Documentation**: Update this document with schema changes
5. **Testing**: Test with both old and new consumers

## Security

### Authentication

Kafka SASL/SCRAM authentication is enabled in production:
- **Mechanism**: SCRAM-SHA-512
- **User**: `todo-app-producer` (for producers)
- **User**: `todo-app-consumer` (for consumers)

### Authorization

ACLs are configured for topic access:
- Producers: WRITE access to all task.* topics
- Consumers: READ access to all task.* topics
- Admin: ALL access for cluster management

### Encryption

- **In-Transit**: TLS 1.3 encryption enabled
- **At-Rest**: Encryption configured via storage provider

## Related Documentation

- [Event Publisher API](../services/event_publisher.py)
- [Event Subscriber API](../services/event_subscriber.py)
- [Dapr Configuration](../../../../kubernetes/base/dapr-components.yaml)
- [Kafka StatefulSet](../../../../kubernetes/base/kafka-statefulset.yaml)
