import redis
import time

def test_redis_connection():
    try:
        # Connexion à Redis
        r = redis.Redis(
            host='localhost',
            port=6379,
            password='redis_password_123',
            decode_responses=True
        )
        
        # Test de connexion
        r.ping()
        print("✅ Redis connection successful!")
        
        # Test d'écriture
        r.set("test_key", f"Hello Redis! {time.time()}")
        
        # Test de lecture
        value = r.get("test_key")
        print(f"✅ Test value: {value}")
        
        # Test des données d'initialisation
        app_status = r.get("app:status")
        print(f"✅ App status: {app_status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

if __name__ == "__main__":
    test_redis_connection()