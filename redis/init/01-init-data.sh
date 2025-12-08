#!/bin/sh

# Attendre que Redis soit prêt
sleep 5

# Initialiser quelques données de test
redis-cli -a redis_password_123 SET "app:status" "running"
redis-cli -a redis_password_123 SET "app:version" "1.0.0"
redis-cli -a redis_password_123 HSET "user:1" "name" "John Doe" "email" "john@example.com"
redis-cli -a redis_password_123 EXPIRE "user:1" 3600

echo "Redis initialization completed!"