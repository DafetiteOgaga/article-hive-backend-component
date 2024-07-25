from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.core.cache import cache
from article_hive_app.views import is_superuser
from django.contrib.auth.views import redirect_to_login

# make it superuser only
def redis_stats(request):
    superuser_access = is_superuser(request)
    if not superuser_access:
        return redirect_to_login(next=request.path)
    
    redis_instance = cache.client.get_client()
    
    # Get some basic stats
    info = redis_instance.info()
    keys = redis_instance.keys('*')
    
    # Usage
    ttl_dict = get_keys_with_ttl()
    # for key, ttl in ttl_dict.items():
    #     print(f"Key: {key}, TTL: {ttl} seconds")
    context = {
        'ttl_dict': ttl_dict,
        'total_keys': len(keys),
        'used_memory': info['used_memory_human'],
        'connected_clients': info['connected_clients'],
        'last_save_time': info['rdb_last_save_time'],
        'sample_keys': keys[:10],  # Show first 10 keys
    }
    
    return render(request, 'redis_stats.html', context)

def get_keys_with_ttl():
    redis_instance = cache.client.get_client()
    keys_with_ttl = {}
    cursor = '0'
    while cursor != 0:
        cursor, keys = redis_instance.scan(cursor=cursor, count=100)
        for key in keys:
            ttl = redis_instance.ttl(key)
            keys_with_ttl[key] = ttl
    return keys_with_ttl
