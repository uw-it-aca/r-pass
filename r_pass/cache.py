from rc_django.cache_implementation import TimedCache
import re


class GroupCache(TimedCache):
    url_policies = {}
    url_policies["gws"] = (
        (re.compile(r"^/group_sws/v\d/group/"), 60),
    )

    def getCache(self, service, url, headers):
        cache_time = 0
        if service in UICache.url_policies:
            service_policies = UICache.url_policies[service]

            for policy in service_policies:
                pattern = policy[0]
                policy_cache_time = policy[1]

                if pattern.match(url):
                    cache_time = policy_cache_time

        return self._response_from_cache(service, url, headers, cache_time)

    def processResponse(self, service, url, response):
        return self._process_response(service, url, response)
