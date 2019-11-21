#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/28 17:15
# @Author  : wjq
# @File    : qutoutiao_wap.py

import json
from scrapy import Request
from news_all.spider_models import NewsRSpider
from scrapy.conf import settings


class QttWapSpider(NewsRSpider):
    chinese_name = """趣头条app"""
    name = 'qtt_app'
    custom_settings = {'DOWNLOADER_MIDDLEWARES': settings.getdict('APP_DOWN')}
    mystart_urls = {
        "https://api.1sapp.com/content/getListV2?qdata=NzUzQ0UwMEYxQzUzNEQ2NzhGQ0IzRDlCNENGQTQxNjMuY0dGeVlXMGZZemxrWlRFMk5EQXRaamxoWWkwMFlXSTJMVGs1TmpJdFlqUmpaR1V3WVRZNE5UUmhIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC4yIjDlwz5m4DTfqjq4sQyuXi8Lz21A2QqzPuq%2FCqiLAR%2BF1Hb%2B3HeQ9p0bqDGrmKHAoxa0CWJ9dYCouiv%2FU4hDDOf8FRMfqnFx5s8%2BKaml4OifKMd8QFDhtZpVQTFLk%2BL%2BB%2BpaKe2fy5j3XCD1eQ1x5OtMXG3n4sYJ2IAMp0gZpifoT9FlPTGMnU3R4Rm%2BIYn%2BnQgAvf4%2BMBxHf%2Fially7JPHij8pW%2BoHDZZBqAkys%2BZ7JfASRAjNkBFA7EEPzDvDBJ8HEGmtrI%2Fff3vGuG7Iv97xePBzp%2F55pgIiAp0ZVoXaMZIzKoYSQY9a329yyVx9NkCwkYUThgQgwySOxiSkeywGNqV8yhQ3iKfQqKguGZ1UELvt6nbkJ4pS0NjkXy7%2Bj%2B1wKnJXP1cAM45HaAxIBFmqhAX3lWAh2uHVBLNqhYnbMeAYsrHcv14wC3JHKecHoRD6f%2F%2Bs9Dhvw%2FKyYtsTfBSqOo2HPPlQ2M2KLHZKtQZuwx82FsWFz0CTfKWnT8TJsrUr0WpVJ%2FtLzD8nIboFA426wa2UOcsfD9CYv7k2u2vdGETtxUMIeWK9yeLxZ7cO3caHcCSILI1Te3yeiXsZmRdtc7kkJvG9uxi43aDwQdTO%2FA8OLvtPO5KNY%2BSRfNWwsUVSFrC7tOqVC9jB2WNgNsXBaQHLq1zGzHO6WJra2pNCW%2FJc1TtYfszpbWGgaeC7UOC6GLXK2J%2FLyUFCNziFutp2V": 373,
        "https://api.1sapp.com/content/getListV2?qdata=MjcwNzc0OEZBNzZDN0ZCRkIzRkFDRjg5RkE2NjQzM0UuY0dGeVlXMGZORGd6TkdFeU1UZ3RNakk0TVMwME9HWm1MVGxoTWpFdFpqVmpZemcyWmpOaVpUSXhIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC6vMWJv%2FWLQjoZ%2B8rG9UlMQVPg%2BVOmmkoUuxA4bIRi9MxTAK4dt08CbxQ11JQCuGBj3LeQ6K3go5C2EJuSXVfax0YEOyc6sIin0BMJlDOKJPgIKWiEepVDTa5dN7lmWtqQKwcI%2FeBLGOxrMpq4YPS256GJaj7SBbxMjAqL8D0qNnB9goQpQX%2Few1Ze7rroFPQXPk1AvmfftaIp7rIHMl9qHY2jxPhRO%2FcUmld5ybIInnrurDgsrkZuUzb%2BU%2BdXuNgdtLcdi85mO5HRrI3Sx3CLoSsg3pUo%2FGssfYGYsVeJsTQJuh%2BbbYv94U1HhwTopnm6xlpyvhlF6OS11jZgrwenGQ28yjlGR4OsWoubX3oQBjA%2Bx6qUYlwcI%2BIkOju5VQdblQbK%2FoO8WmUQoGaZmSCy0G6VVd3OlKGOrW%2B0dTh3%2BiwRMXN9w9Qv7vvwYYEa51stFJ4NXpzyDOhH3e8IB6upa01dkAfdapQSbU5rxzKtzOAerXnMZ0lcoi3achvsRMqmnMEDDCk%2FvDqrvkZcSobiqfQTvQwPrO4GJzZkmLRlOYF2tcDFMwSK8GzFm6%2FxsHmwom5yPXD7rHK%2BssluVdIZQUqOxEplv0038czhTjTwkfBFcgoLzKGePc9xrJNHzH6mTUSrupNdF3oHEgJoHf5P0AUQva7T9ttswf12E5VfulqSfAY79k4s4MpK6DrLtP8n2GlXsFHhh9NWlzwYf17bvOqal": 374,
        "https://api.1sapp.com/content/getListV2?qdata=QjA1M0RGMEQyODE5NTFBQTA1RUI5OUUwNjA4REQ5QkIuY0dGeVlXMGZPVGN6TkRVeFpXTXROMlV3T0MwME1EWm1MVGxsWW1ZdFpUUm1aalkzTkRnM05tRXlIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC5VzjgliB2hpdl71eQgbheerWm8dSIv8fP5pAry%2BDfkCKUrLfSueNnNwXV97tVD8bX4iRFLcV5%2Ba55FEYTdDTGz9UcGMHJmMGlCU8Jszx2XqbXmFl5PkbBiYzH8WKf1OQD7mu551kx8Uc06FP%2BZIF5SOvO5CCtvqeZQ6d0pagUxe6NtyVKStuM1vdFuNNEAfUgxnXWmQHtr70044Epzx19j3wFrbswaEpUZbyT4YU4cw05rvWLw8%2BikLkXiuPoQHL6MTJj%2FwNW3BhjuDe%2Bcr4QGlx5cMUdsgs2Vp1uWv5DcyRLgxJ1ayfnKiwnCOwuFK4wKKac82Ws1q9swLrnO%2FfGU%2BzSIQQanFUDfjVoFurMmpoUA%2BnJM0aISmnr1FgVj%2FlvcrX932koZfF1Rm5szM4%2FUBOT5WF89%2B4qAt3GtJJUHR5zkuA0re5R3Ha158MrRqWrCl6Vj9i5BXRIPHyRh6L8ZI8aSXIYqQfEabIS3YTApMQUThzD1uHkYtjCwlK5vh2qmtc4QRP39hYo7R1%2B56onIF%2FMD32S7ruARUVAuegq7unoJpOwSKQ0oS0eMlZzYbhMX505Z0B2tlmqXeGMioo7D2fp%2BiLRF3ZQEMgQuMReMmofXdlG4wNVFztyf%2FKFKAcMywfdUVuQ1VFlMuzwgfZojqYz9IboFlmKNx%2BuVKKwgpkiaJ7oH7z2B7O99UbdqgS9EVqNBQPZynhi58NiGpdqAbYDB": 375,
        "https://api.1sapp.com/content/getListV2?qdata=NUI2Rjg0OTQyRjdEMUE0ODg1OEJBRTcyMkEzQkJDRDEuY0dGeVlXMGZPREJrWW1JNE1tUXRaR0UxT1MwME9UVmxMVGhrWW1FdE9HWXhaRFF6T1RFMU1HVmpIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC6rlGp7GLZVvw7wbtt1i%2FwAsqxuD5XFWgOGb8DPRWvKQMpNQfigcyT%2Bf4MLAMAp5jP6RyG0pEFDxKacdRuv8A2gzCKdsXu4JhMGf3jV7csLR%2BxUihFvDxygnM%2BdP3qStsxhS1x4V5nNcAvttkS0VIP827xI4OTMdysJGtQWsWfkumyUZLqD5gXweDumB5v5L7gWix9%2FD0JLRjYtdjQPfxFqEmLB4P7CvsXrvVOecaIOmHKC%2BgIecvNLf0IoVKun5UThT05%2BumC2kdPJVJU6faDTyzHq6o0vi%2FCzWUdQZYtWs9weL9ruWHL5HrMkvTBtbFIKgZ%2FiPPjx%2BPmrHmGjYtdqdh0LzSP%2BMLltkGrbBnxYKCt0ObRmc7Bx9PYKRRcujfLBykXHNv9ZIj%2B8JaeyloGU4DwvafhglqCKxdr7sIwcXzM%2BajvAJsknAi7pq6npzgz0E6peXFcP%2F7%2FelMRBq32wFkpr9jPLGJtiXV6llL8mwwJdATaE7ZnzkNnvcxHPYR4b3yt83jUMRmQfzWomGqX32m019KVfHtuTiEt699bbcpdMmTZuQg1zsNsfngLq7XWNtKMjezQAS%2FMDqvbGsbqWusb35s0SwQiY%2FYw%2BcrYWE3wVhw%2FNm42MVN4SBA%2BnAg8fxENpNJEzFq0nh%2FLbSrIRzNMVdspanDM5u%2F%2B1JClCb1HjizRmlIfmMCOkiDVRkbGKXBQtMA07R8wIIAPaYvYGjMBf": 376,
        "https://api.1sapp.com/content/getListV2?qdata=OUNBMDY2MUVEM0JCQUIyMzA5QTRDRTVDQTFGMjg5NkUuY0dGeVlXMGZPR0V6TVRCaE1XWXRZalpsTXkwME1tTm1MVGxoWm1FdE5URTBPRE16TlRBMlltVTVIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC4g0jsSQlzcmt4fqwvNZ9qxNCs31Y2ZaUpHQhL8DAGStghon3YQbepQUwn8QHqU6y%2FXX21pL4lQZPox4c6zl%2F0sIX2NnSSO5dvkWVgxCofA%2BLuP9dnMa1bPJDjq1JNJoZfNqk17qK45SvlL0LNC7Yql9Gq0M7aG8A%2Bz%2FCsXNmssGhKOQajWr3ii8OqQgAJHmTs8kxeKTqYA%2BS%2BxBus1uSCPZ2fpC9j3WdK6GFvD84Sjm0%2Fw7xJPTmrwbBhbViX4%2F3MLR%2Bkeevc%2BNu3pUI3b4DjF5AXxuRANILSX5k3QIxI%2FPsGO6hHJm7NLSo4SCoHPeh2VOBrD2w6MXrXyry%2F%2BArkxJbp4q8BuJR46GZ3Eo4YRr2SxpCyXwW52Zblxhh%2FuZKvD%2B1hFLJkbbX%2FpS3mMn6rXQNM1vW5qT85hlkWwNeWiOP209FBFN3C5JYSU5kTe9OtG%2B%2BjAD%2F8JkXY93%2FP1dhvuq%2FkUBmrdimnOnbTCeQY5FUdV2l77WodR7G6pvtF1Fh2MmiSIgyVuJ3LIAUX2fAzApHFCNAxST3bD8f1SmM3JJ3ZI3HhQiYkxRIFDq1OIo32e5Dms8d67vZ%2BqAo1QgC5mFrA7pdTlLbrowr7%2F2erA3IZfGLmw2ysBYRONmFQJ5xEIbcMSjhyu0n%2BlfRhDFkV2TpWa9oBYsuY8mXMRbTI3VVUgU56ZOFtD%2B%2FXJ%2F47B4HJnwkscp17FlVBQDInwFlgXmlXt": 377,
        "https://api.1sapp.com/content/getListV2?qdata=MzNDOUY0Q0JEOUZDMjJFQkI3MjhFMEUwMTkwRURCRTIuY0dGeVlXMGZZekJrTnpBeU1Ua3RNelV3WXkwME56UTFMVGhqWlRZdE9HSmtZbU5oWlRCaVlqZ3hIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC56CoLVq6UbdxJMqGVyFaYRgmmr8a7o%2B2%2BzJSKsqkSdYLO%2BJp9m98ZrSdcCOUZUPWTmL5Oh1cP5GsNMih9tKMtBdkSzTSX1%2BIpb237se5%2BALkVOyoYKa%2F8A0Vc4cj5o8zKKtuPLMzMB0BRDxK6DMvXR7v8NwVsa3CNlftP%2FjU1rpO2IQ%2BbSoA%2BMHnYNq12s18jFp5J4IVd%2FNhP0EhpusAEebyi3pbPdqLHYOEPwmVWOugEq4yNJpv88CqNT0pD2fAucgzFE%2FgthSgOCfHud7FamjpYQNz0t1L9JWWhnM8bvYEwdemqUURkeAVUfzipTByUCUmQBJlqJlbELFXlSYx%2FkoB4j4WK%2FO%2BQCdWWdUzJEMKwzXgZBjt3iDNplGcO%2BFPqsw%2F4bcbtX8SSn9SiQ7lBivE7np5dDBxBKETk65oHUBy0rTumlC%2FtH%2ByyWMbCJ9dp5irkd4KOCn2c13paNZfF28oR%2FJcCeyXKpl8ZiTZAcroMLv8dp7Yr6A8zGvGmgbNEPw0YoG5lhD3YFOPqf%2Fplz7jDWYlJFMtrqqyKjI06Yq849%2Fu3x0BHWDu2OKnFZpwIelkWh80MhSX2%2Fa1wKZ2qNOYW4JIs5A0kyz2ILXgF1x3D%2FFICkGraWU%2FsgT0Yv7ev69eoN8%2B2FzesiXmvOo3Cx9n6PxejYUkKOYLoyyGrnmRxMUViDPK37305H4%2BJEd3Oaqp5v3Krm15EK7nRXsW%2B1hWpY": 378,
        "https://api.1sapp.com/content/getListV2?qdata=MkU2RTQ3RTNDODQ4QUQ2QjYwQ0IxMjM2QkU3MDZDMEQuY0dGeVlXMGZNMkZpT1daaE1HUXROek0wTVMwME5qVTNMV0V6TTJFdE16azRORE0xT0dKbVkyRXlIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC4xYwt1V61A5FKSaB572BwCdq4Bi0aTcnm9jOEizzZ7Vu188HbNQX7bDNEnyqa3JT%2F%2F0O53gk6kxMXDtUI1OzTlT0DmMDVkiO0McRNIYuHBlV2egVHCGQ3buTw2H8g4hfTjzxg2iZTZ28TAx4mIgl0uI2W49JGM2HB3t9110DA5OQmn2tqPLj0VngutyIBS096ywDSMGogNVq4S00o0%2BL9hsvAFiKtTTn4%2Bn%2Bhnq5UfJ9PPUM9iNoRGsv5jXkvZf%2BwEcMe%2BYui5e0vnQT8htnrK7f8RwdQXYwYrGZuYG4yXIYsD7NLqUJqaRORP5fROT3cvdKSfxH0paCsIWcI57tOjj3OjGxuN7ie4uiFh284b72EjpR2TXSe%2FVvAEq5ri954uMtPEw1j%2BQ8SGQl43vrlyr49jxfLEhAh2UQuLwefVJwhhxE339lqGu1ILyLzHg9QXuLyEpK4rufycoyhQbjOzwluUNy%2FRx8iAysJ5bvEUDMEYjw0yM8eZS36kuZzub8lMlHCrtjNoUaHVuplszCKIyUickPHvJQLsfRI0qGazAvxnGOgBzCDe9iKMRZ5rpGIOuI4JG%2BVBUCin1LyKeBXYyeq9lOvJFefkp%2FyAa0cK3itwzOyfF6KUqft7Jfum8hfrS1Mvhvyg05EvALX0wYCpHgdHQj%2Fr2ZiKUpDkSG587ir%2FIv%2F6cHP4DcfqkfZrxTDYVVT6qadwxTtCkQJfnMzhYJs%2B": 379,
        "https://api.1sapp.com/content/getListV2?qdata=OUQ5Q0U5NUEyNEUwQUMyMjY5QzQ0NDlCOTFFNDM1NTYuY0dGeVlXMGZPVGt3WVRZNFptTXRObUpqTnkwME1tUmhMVGxrTnpjdE9URXdPRFF3TURNNE4ySTNIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC7OcWOKYmfmSHGtPdtEriuL77eKHU66ZikJ6I1%2FvY0ON04L%2Br%2FyxrTPbFZDrET72nBLTVTVThyuMBmbY77g%2FvIeJ8%2FcUiv1ADbyU5zR2jkgUmBq8oxFeTz6W8q4YrXBzK9L7Dw5k%2BP2itasOfMdQEioLotPYEsI7BqeSm9ZLsj4C6gFx9VQyd7mpX3Fo300Mh%2BTsP8Q5kZ0rwgrr320MaK1YbyNWiutEw%2Fdy1DPTgir2VPqHB83iRb2waVsrwU%2FyigV53N7q6%2FRiJvn7ecOe3YMTKxHmsuJZTSwZ%2B3XjHv5RFFgYTgli%2Bxx7gBqZE1OAAgrqOEp13yJUYcks9vzZnEvNOnUyA%2FsfUbXFzcVGsFdvEQFAVcufVEN9PjU1kwDqU2J%2F31uRcwHkdDCaPetYAZ57IEIfS8S9IBqO7SgjtuCrFikrd9xx%2Bph2h6aVf2tN5tjhWtK9BADLnsyXZeGB7Ly2WRggjDNkahmEzwj6VdAVhO9%2Fqa7VzUYNiNxPqR7YRuxXlzGlTlL9FjgYlR8KO72FVgkSaxUBC1c4yf%2B%2FWVRdUMZvczoEMU1alpO5Cv9L8AU3VVAMEHjNQ9juuE1V5HF8VvBpe9o5cF07PEfoccpP7Yv0rmoc5nfQzng4q5FSupnw7x8hGnNv8ze67LP%2FjNvChsA56Cu5iffjlo6yrUjxVm8oJcXWXNAjuE2tcSWVxcDPaLi6HzM0zIql8iDsrxTSdta": 380,
        "https://api.1sapp.com/content/getListV2?qdata=QUE5NUZGNjZGQzU5OTAwQTAzNjMxM0YxRkZBRDQ2NUYuY0dGeVlXMGZaVE15TlRVNE16SXRaRE01T1MwME1XVTJMV0k1WldZdFpUSmtZbVUyTW1FMFpEaGhIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC7z7fI%2BMo1l8%2BEbtjliOrb1gx7r9sn%2BW%2F5SX4cp7tbx7D21v3FA4gNR4Sww9hJ0mj4v90HWX7fv06qLVUfSlhEwcF7QkDNqwEirB39ZolgjTnrmJEJ9lCw%2BZTFR%2Bz5asF8D0oXbfzeU6HQZ3PYS%2BaecLkxkxDTeBAyRBPrXQFKSOFbnIWHekc97ATPJ43HMPOYB0jN1ZVyum%2FzNDAdCEvsyjb8%2BSW7w0mE2p8dNckkCGKCpBPs2AcCY4wqRAAUz1c4SxqkC%2BEnpM%2BHT7a60AvOjhJRZgZy92UPaYtYANni5aPoT4Pks7NCRV0I%2BQfYjaKsjIyIyF1ugAaMHUwWNcVk%2FD5tOCGV239FxEClTtrd4co041jcnMScocKX6c0BDVmcraqnJGaLHr27kV8n38TCMwuW7E468uLMgQuXefysv1DKMnrqbR1Iw68eKPE5vk8WQJFy1MN8Z3lBasdTeyymwATe2PPwIRtpC%2BT35bhUFN%2BPtp6GW62e6XisQdPyK9x27EowT50iuPGGG4AH6%2FaH5F2W0gZZNJd4aBcdyQQ7J%2BHLmjzhBKt1OqnjlXtDjXm9aIzd0mN1ddik22FLyVpklkpyM4oHa1Bzosj9J013%2F%2B1qHjmvlhLbMDQovDmZNw12H6gEHp6WkkNCv2nd2VOTilZB2RBwOVxO0AX3crFudumgFLF8vSdwxZ5oWe%2B3OaeZZNUBfRAekrqKlL2cxv3EfijhY": 345,
        "https://api.1sapp.com/content/getListV2?qdata=RjBBRUMzN0UyMUVBNEQzODc0NTIyNEZFQUVGNzdDRjYuY0dGeVlXMGZOakpqWmpsaVlXWXROMlk0WmkwME9USXhMV0U0WW1FdFptSTJZbUprTlRVeU1ESm1IblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC4056AiIkkg0%2BuebbN2nL7%2FOvvsJAQOSZGPB2lRtxomJi3btbadmUEiV9YKPBt%2BRstlSJ13nHJyo16%2BkG5Gj0bdpW3MT7Q0RmDw%2FYpvP%2FsHp39YzZOdNnJ98NQUW5cEDbbQtqoMzO9Kd0%2FVB%2BGdcWZVlN%2FRJfMd1BMX52VkLm%2Fy8PL8M5ANXM80VC7QWDh%2FNtRyJQn2O2Vm7upUpmju8%2B%2FAQGb0k2qjeGjs1xeZdigwCoQAarFFcgvfxfiqPMw0IBEFz73VCxJ%2BcQxpxfpakAhmabh%2Bn7%2BYp%2FN17O7FszR%2FWcuBSb4uUpB1KgEDr7npEf3L2534TrNGr7F2glJwzUqouwAIZjli%2FHiW6EHIDa3beBx0NGhoJo3pA5vLKiBoKtkNrj9GVCiLV15uXo926DZigsQg1RfOrnwrTn7wonm3Hjs3avboN1%2FvHkdR%2B12d7Kk%2Bvqfgob19X%2FYcngWJ%2B1W0Z6QuGZR1sG9Qz6HTW5I2DHdCB3jvSxGJH5K%2FnQLWXKzuR3p06NXACq5pTVZ7XitWqgvJANy6SsbiG%2FFTui676yfwobL6iQxYuu16OA2LFMo7e9N0wC4lyV68RbewvQZv293ZIrqcH73MsrC646EDTaxYg8RNTe24SF%2Fc9hZS5eLwhIbJ4o7yXY4RcEcWZRncMBDCgXVmBsS4A5kR8kAc9LS9rWLW%2BmiR26Chk7xk23jEWv%2FqSwB2lyaxoP9CVlmyiWj%2B": 348,
        "https://api.1sapp.com/content/getListV2?qdata=QUE1NTQ3NjVENzBGNzczMTBFMTE4RDlDMUIzMDM4NjIuY0dGeVlXMGZNRGMxT0RZek1HVXRNamsxWWkwME1XTXpMV0l3TkdFdE5HVXpaV014T1dRMFl6aGhIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC5I0F3GP6kPAQBQ5xU8u8SN8HV566rRCHIibY1vPgC5AGJZAgLMCtt%2BAHSzZEKWVcGpDT91htmWD7RPRrB1AwljLkto03%2FXbGo%2BE5pzffjPNjqcLsRZElfW5ACEnG98afeOkOZmgp3sqLWAAEyc7U8qnKsk0QVD%2BEujCrGA0H5fNFLyvF%2B2sVuyLhtu0GQ0%2FNqwcSnet5Bly39v4N5hrVVWi3x8W7B3ookpUPem2%2FTSHffKYysGgP5Ih7qgp%2BCH6%2FooD1a0%2B%2BjD688J8TKQ5jMQHqBHfusvxu%2BrcPp1dcZU2BoPV5qMVpMm1p6BDLRyPSUVA6eJmjv0JH8mVfomLbRtD3aF2UNlPLzIZFErCPQ7YBE6J1%2FGLnDlnMydIpmrrRatS9pHUKVqez2fwxTjhB%2FzAelESdEsdgXhQHk2PI82i84MoN2c9%2FbRDwMT7sSlD0azM63iKabTF36ZS5mv5MI7j34v%2Flqm7ppVCopBnOZrYksWNrFSUgafHladYPo2TfrAPXTJyP0PzoWCSyJEl5hbhW5KtPeMRWYH9N5V0V5dBWGm48QIHLLx%2FUQch1OhQhLJrVci4L9%2Bgccz1GXxlZTSi9CEyYxZz61JL6dyzm8fIgT1FmiWyPbHMDBzlMlgcEnHo5ZSo7uth8oOYszfAGS9VLC%2F3LXWGC9RO%2BNX%2BxRxKQZkVpxWkr3zdgjzwH6Bja0U%2FOTfhGI9RwZQImCtQDz%2BxklpAgnDtPmFs%2BdiiScDKkuZaQ%3D%3D": 350,
        "https://api.1sapp.com/content/getListV2?qdata=NTY1NDUxQ0ZDMUZGODQ4MTc1ODkxNDM2NDRFQzVDNkEuY0dGeVlXMGZZakJoTkRFeE1UWXRNR0k0WXkwME5qa3pMV0ZoWldNdFlUTXlabVE0T1dNMk9UZzJIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC6kqP2cDTWSM757XuNKMUjBPJrhO881r3iuVHMKp5T3dl8CMdCWbJO7DMAJ3eavCElLb6L5qf0LVgAkh%2BJiRXSxdYcaPPJV29kjEIfx1grrpdFEjSqj2KhSu6FXsS2g%2FzIdFQtDrTpvAiJNkpwQKsxabULbdiSPXt1koF%2BNFnWz%2BNEU2DwMFFAoml%2FLhDDTSsxP8CTuyiYZWV1I66ZsPekcE5f4uIgHTOv9BMbkFko3WEzYA6G7WxGJJFp7RR6c1RZRFDToXMvQ7ljRsJLwxxOyPB5KsLB0qXUlpexyKxthOESo7zmBk%2F5vbN3mrJw%2Bt5q1VGSLp3WkZeTJgXOMOjbSqv9Y%2Flsf0pLb1t%2FsTEUl4lsB4EWKD2eiuVdiXtqngfkHiIlv%2Bl14z070SLTx4vk%2FNBEZUP1HW%2BvTqqTclSqzbeKRK4nYYai3TMAQqeFNKZ2EU9B5Rc6pehsxPvn%2F8mzCRx0UYCOjzZS7PFVNEhtf9YL6wjtdWrFYHKt9JHLh4Ttqk9uzRdHcR7l5Wmi9FoG%2F36aRSmdQzBcdh%2FT7J43HPFZWxwmD%2BHzd8I8nWDVZhmcUPeYJfYqdvGaiMAUNsWUHaDcks0Vr6pziDh5H5Kl8Uj4dUb%2FcURqG6FM%2FGQCNnr8UZPmUi%2BPR9pggmQcR1OmSvSx6zqmfHDdTNBjFjg0JFVEMYAPBrXgxH5Em5GXpt%2FHJI78%3D": 353,
        "https://api.1sapp.com/content/getListV2?qdata=NTA3QTQyQjNFNkRDRDAyMTVEMkEwMDEwNUU5RUIxMjkuY0dGeVlXMGZPRFEzTTJVeU5tTXRZMkZpWmkwMFpHSmlMV0ZpTVRVdE1UZzVaVEJpTlRObVkyTmxIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC7nwNfLt%2BoqH%2Be6pthjJHp7smzSPMNFRQrZLdBCkDse%2BKGRnmdEPL5k4f3JG0emO5uGXUgeXDU8DiQX5NtCMBfSsQC2AXt01uj9o2IDr5vGdIr9v%2BU3lXE9Om1XMPLEYiTzRjobu%2FFuV13VGWeKwUgtyc63HRd86OKRiFHcPJObNcm78tacWEpiSny9k54U0xMh4PZ3En%2BW18Y1%2FaS9TUiadGBidJftrrtJT%2FG2mysTXqLTHyBsI6fv0DiIf%2BtOLKrxNuej6%2FRrbExfobWaatO5D3qAQu6YIDItJsmCL0h0YPMHjtP7TLTTdBjr1NrTSt4ykf9QVQkZfS3OYcZ9VdXxQ3RNY%2B%2Fu09R9%2FwM9DJNm84TCvEDufKPNZlHIwxzt61LStvJAnRLqh5nYl21cGETtpyzn1Jrl8pkeMwDymCc%2BAvzOE26p6djMZd%2BC30ULvis9c9zdvwtxNzm34m0N6b7xghT9i2DJjQ57v4Bn%2BaXV%2BCfHWf80Gs0lDmQjXuD0mURp8EXac7kq25KqYw%2FDo8G%2FqEk%2FrSB8Yp0ckLrRN4csZ%2FqjK9qCT1dM883xhD1N1HK51nTsbVK%2BBCRgL3At%2B3xZENOlvyvy4nxDRoRs0f5BaUpaQiEbKKpao85N0YKE2coj9Zt5%2Bc2gocS2%2BPmOr7VozJaeMjOsiLXTFu16NqBEuNxOmoFRl3TZbwi4NFMk%2FDLmBqHq47MSYJEtnucNPWbVdXVgcis3ytu7oRxxFepZwQHuiw%3D%3D": 356,
        "https://api.1sapp.com/content/getListV2?qdata=OUY3MjFBMTg5NjA3OTY2NDFFMjM2NEIzN0FGOUQwNDUuY0dGeVlXMGZZV1E0WmpObU1HTXRabVkwWWkwME5XUTNMV0l3TXpJdE9USXpOamhoTlRjM01qazRIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC4LuAL0FgNFSR%2BSjt%2FKDW0a6eFnfhILeTwVqQkPsAOS8D6QXJVAb7sDQ6Ie%2FBSg04%2BlQ3voWezHZlhjSJIW9lqC2UYGF%2FQdCKe%2FZC8nlZs0NIEGbxBPs0bkg9EZwdnMJP1cZfVWZ9C1e5XLYAtHfgS2exlJWn782Tr5EMBXsFeh%2FJTskNCznfCmP7XxMj%2FT958dFz9s0wa2WMxuXYAxxnTIyzKG9m7isJ%2F6xC8MwlSj%2BLiDvXmlikF4SaEgm9XNR9I0OZVZN0Fxcv1oh1LPpyZpHCdqdXk04pwIYBPjbFVquk%2FwPmmUV9y3kzxmU%2BXE7q%2Bjj%2BpLepgI3M1bSl316yHA0jlI0aifMZcs21YTroSxuyfC3a9AIAKeYj0zyQqDAwFM4a%2FnPMb01bS%2BUVgjOKxdhvjeFBv6udy7VfcShm%2FBYh9gEQvQ2Ws1IJOKUjsZ5rklKYyekAkYNYJq5hNJLFjxKoQ%2FqavREHNYSMEuN0xk6y4RPdUxsXpWsOPlgDaRmO8aj8Wl6tvxy5n7gvV3TfGmsdWnYaWED3TOBokUKU0yGCfs8gZ1pFRwHFAkx91lCeYavdE7ScMHT7jiEy5f4n27Qe0Vl5gi9wCx33szMS60H6wVmafyaN6Th%2Bc0nD84kkDWZCybz0pg%2FfUdrN5XB8UYumThItKucnGqyGqKpQyi5Ccb994DvLuUhml%2BMaok0p7ne6Iwe%2BsMf7wyWQLjW983cQ4F": 358,
        "https://api.1sapp.com/content/getListV2?qdata=MjY3QzNGQTdCQzMwMjc5MERFQzkwMjgxM0Q1OTIxRDguY0dGeVlXMGZNalJtT1RFNU5USXROV1F4WmkwMFpXWmtMVGszTkRjdE9EQXdOakV6TW1RMVpXUTBIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC7IlaY5MEazO3saGwJ3Pxo6UUl4RDDLHrGI%2BKH9zJHwW90p%2B13Sul4TljiwnnwJUm3WALC1MhMi7T2bPJZO2YSzckOWjh%2FRYHiNYg8FEl0OlwIiw%2BxLnk3t8nm4D02Y7V4y683al4YSbmedxxhT5pApmW07pC29V1byhPm89w1vdmgJSSSOX%2BuWIGBKLBHB6dzoniafrdaSzBhWAGwKj3SBvgzuI4gir5o9u%2F2Pf2yTF6HcXUBXFsC8da1%2FjeQ1nEOB0H5z64hDthRhKJe%2Bxzyt6kMkePYbe0TMjAzRKw1BopGjYf7%2F7cj9LMpazatwVOKqMgrFA7LwA5TD3g6tHmpSAeel5OIcJLyhYtw1JP6M9zGsjqRgL47hHJPIMDER8f5YLS%2BbofhQh3sUV%2FeteWkYOtDuyhW82zwXZU9C3oh51nk3neahET5UCJo8OxjQ%2FVNV57eYL4uSApGbND%2FXHbf52RaNHNh%2F%2FL4QZimkCdv2jcPQ0iaSa5EvZkFULrAgfZvb28dca86P1kTwxPPJC%2FIpYFWYRSozShGgQh5xUhkdzpPSKX%2BIqRpJ2nSxke4DdNnhwzn6E%2Fs3bP7Q2eIr%2FrlEhvo%2Bmvo0%2BQCQO3SZvRjT5xUpJNA%2FSafvriapZ4qHVX0JbhpUNPHvXUXKFCFCEj7T2kx7%2Bjxu6cPOc%2FqcVKrljaBrisua9baAW%2F3kr8zlTdgb6qRXoE5ULFpIYU8RYyAZn7LW": 361,
        "https://api.1sapp.com/content/getListV2?qdata=NzNCNThFQzgxOEZDMkU2MjRCMDFBNTIyQjI3QzQyRkMuY0dGeVlXMGZaV00xTlRreVpEVXRaVGt4TlMwME1qQmlMVGxoTW1VdE9EZ3hZVEUwWm1RM1lqSm1IblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC7dC9hthtFtZytZlC4EFxilB6OV1lTyEsswAPgthJatDE4ycYdgY5lL4HDAKWoPvZOql962YFsl19mYT36g%2BPAAV4KriR%2B3b3OWXsiGq9%2FN7NVbAiHQ5TIFrroOlpwm%2BlrKvUIhoSdehztYpEjVOjXPv2yZAw8kpsgyVQirmgXTLKsgyGok0WDiGhli%2FH%2FUiEMFZKY3V%2B4HPKgkbCS4wU1bAWXxNk%2F9bFxBXYOoxO7hCGdsimA1pfn81cRT93L3QvjEKL58Fdx7%2BnQ20%2BBt92kQLmI2tEKVurSqa6C9O9Qe1SiA5jtuqPHl81m5B5WmpQ4ofhE2RwbAy5gUDipMD7pWamjJibKLQEQoCOcYjG3UN%2BLJpdHb%2FYqM%2BEkE90DeYQJUZ4E6kxYFqqNQQOXlRKjJ5%2BAAkdRYc7dkIjfnYOkVh5PbN%2FzgZTR1TTMTNyFWC379b7yTRyi6agTh1a%2BOjh9AgEOaRwRoI%2FDv95Ge3uXHf99J3MYE2u8ZX%2FFFwkftV0zSFggfAF0eY6UHnrI%2BEOCqJrRv53GMDFl9zTtTeZwsRjh1Sene9JJEQKth%2B8y1ojLhHpSiuMap9HwMYCpA4RsRKCT8Y%2BZwgHmgnaIfXlIzb%2B0MpmTmCy8mz5TIjaZAhuagVqsJP3qvq8tp%2BkCYjYd3lB1g2Nxhh9YK6gEK8jPtA3ZhHBn8Vp3DrSTz5xvdOo8sx2lZnLYhbEQgt%2BLoxt5QElCq": 362,
        "https://api.1sapp.com/content/getListV2?qdata=MENGQTZFOTVCOTA0MjI1OUVFQzkzQzhGQkVEMjFDMjAuY0dGeVlXMGZZakZpWXpaak1UQXRaRFZrTmkwME1tVmpMVGt3TmpZdE9UY3laRFF5WW1JNE5qTXpIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC7uLKk4grorwJ50xS09UPcur8xEspkhqQMpmtgyFHl5OB9gU4%2BITytwYfxCY1j8dqC0O3tE1jrRB8S7Gs72G8FY0r9wDUQ12ZaqbqHrl8ONAoq1wQHt5Vb4F2cJaaxBGSY8OCAaoycHGkgkJ4nxtudS8qNfYvSKL6HdLtYgfXOrr9SnYANkojh06UZStpO4NPxWGzeJQ2pLqnd4EdjzemnOcwHtmhgJ%2FyYoXPEz0uyhSQCmdgPp4jNs%2Bd%2BmQCtUK%2FOw7fANBWNmhDD%2FYJMalG10RPqWC6ExduaYTyGkbbOuLL5HVMkSyRF5GuKKUBzyXTvmzuPBxB0Wie6jl9HaOBtP2kZbHPT67Thvi5NgvItLKwKs3X1V%2B%2FMlI0jgwb3qYsnZwieRkFqGnfnY3hDa3z%2B2%2FQ9P02%2FX0AGOmuevHcGd3Hb%2Ffq6jQ2%2FhSI42h%2BbimBQiSFaJsIBGL1QuzjE17zYw0tf6k6ed2ivWgbcvx6Zy1dEfDYlfVo1SHXSMH1yWWhqWnE54pVH4jmlZgFp1VV7ptj5epdIfg5Hh4c%2FqvOcEOw6vyBWGr0EWupOd2XPNfHK3IbzXVnq5Jml42GJX7Zp%2BaTnhVZN4sdoJnPMJxZWsgR6ZVqaWoYeZb3Pctxqy2VGuZWdnV%2F90KReCAomDVM3pbuz4KNtKVEUuNvT5Fys9vw0Kr3TME2dKeZsq9EDsIt72i3PLwQz2D788WjVvk7p0OzTi": 364,
        "https://api.1sapp.com/content/getListV2?qdata=RTBBNzAzMUYxRjM3MTUyMTJDN0NEODJCQzgyNEE4MDMuY0dGeVlXMGZOalU0TjJNMk56SXRNelEyTlMwME5UbGpMV0ZsWmpFdE1tWTVOakF5Tm1KaE5XVXpIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC7Jh%2FOpBdbwLZjcdBjwPVDlJqullJ187iTRZZHcC6gv%2FnlVdrwJOHSX%2FcNpyBng1zbEbDTSWLNBh43cOryrj0X9r%2BL5ro90J76EMPjI3MAtddm%2B5u6eItK%2FYM8Rj7RwKVZ2XsHr7m%2B5yGB5OPBMXwLl0XGdIeAyLrTJFMKejFpe5GlWrgIcapoX3UguVizCr23yNwi0RxGVoE2fwwSIzCR5u8RLdglsjXe%2BIhu6na%2B2rzBrLZBk02HYJ55s5ktetR3CA%2BwbX0H%2B4UKEBIkTje3lcahhoCJmUrXEV1wkqcp3QQEtl918FOx1soJOBTHDSHwYS3U7R%2FBJI%2F1O0TonXcpRjQgMD02oKIezN8OV54c50qtg52YqQvh%2BPrj0wlZUi0qyzDfpCpO9H9ru%2B20feP%2F64MpPESH%2BbCQf2Yys3wu14oZsCfmag39GqwJqoDrrA3Je%2FEpQZnuooJk12KpHuHD8biO4HooMBOJbVFiOptHavanV0kTYQi0KEfQbWnNdyo2AQNEpxLxmhJHhco6iN4g7tFD0Mpdpp6VcWbySq2lbfB8ep9lFpB8QFh8wsbGBN8p%2BNWvFRaq%2FQOoO7DLZ4LhdbbGK7uyC6GYj8H9uL7qU8rxp1A5aDd1paTiGA3imnXLLH09ZGraE%2BnqCw0XcFIMDYQGfexDgJQLB0eDoovr1dMHYCQ5s24bThmjQw3%2FbBLI%2FTCAYj%2Bb%2FnPGn1Vs0maw%2Fdh1m": 366,
        "https://api.1sapp.com/content/getListV2?qdata=M0I4RDg1MDc5MkM2MTE5MTkzOEMyRkZDNkUwOERBRkIuY0dGeVlXMGZaVGRqTVRKbE16Z3RZMkUwT1MwME5XTTJMV0ZtTkRjdE1ETXpORGMzT1RnMk1tTTFIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC7ETiVvpUaW5Up4PtwfY1Yh2X2ydrxozhE8kjl6vi8UrwkMXN9YXbeF%2FpWy7ek0szjftDtUYZkJpVO3IuJxdGAa9n9gM72LRsZxBYexuLZ6Bh5ggZ2iBGObHuh1qmkP85L9Hr0KeJklMy3H1LmKbgpUdgZmm62OH3QHHQKNRu3pnzlrQgvsL9%2B99aiQrh7nd%2BnWd4%2FcX9nUgHOGkASdJYobpsSjvlfWrTWd0V0wEDu9AchWti9UaP0jg7NqBdGNYAtOZkx4QbZp1gZHxHziL8%2FCyw4Pfwgv%2BskxdjBxhsL4%2F4VOQ39dgvQHuNrAqRuJV9XwXvz7kIxn5gJZHVbfIfClMU%2F8aG%2F%2FXnLsTsDgCqTDsbLpST57X47XRKSmkG1PCgj5JZd%2BgaXFjwjqkaZJhCHZ1FRSugPdb2JC0sTAHotkUkV11Z7LMk3JboeZpenT3vohWqvzPZEQPH5pWL4iyJX5YpqBo3aUJTwMIM0rZdkO5K%2B21HvRY1atJ6riDvlDL1%2BVLO5xxt20VJZKcZO4VkK6ahtRHrasvlzWPfm4UPXg16jHuIbyWk1njsPaDTm%2BkrVJpVUgNnv2H9Qh6KjAu5Te2JGhcBf72b3UiRsv7cUMjtNfLKcpGNgAhm%2F2Tq1aBnOm7tN75O3Tp5yDC1dSgu0DZZ8yXlKVz7X5%2F3fqM%2BJ0CDTHdgJvlFe0V3ibdd1LMl%2FgJtHbrhGhWV%2B7SoEtFDT2BTUp": 369,
        "https://api.1sapp.com/content/getListV2?qdata=MUI2MTZENzU2RDlGREFGNkFGNUU1QTFBRTlFMzM4OTIuY0dGeVlXMGZPREl6TkRVMU4yVXRaakppTXkwME1XUXlMVGs1TTJFdE0yRmhOV1JsTW1GaU9UTTJIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC7BeJD%2FdHE3BoQ2TFaWFKiI6uhfJfMwxcG5mKmX2Q%2FV3lmsRTIuD3NUO3YHbjYfn0ARPAUk5mXtvMvOSJLHjsR7S%2FvlxH6g8J7nbRd9e%2FoWDZaApqJpIxvOYx3Bbokts99aooyyxzvVVERO%2Ba32L0fC8DDBISbc55HqDW85j8fdAKqUQG9pIa3D3zlceQU%2Bj%2FeZuTibPUZVD9Gd6zRFyK%2BnhHZST%2BaijEZFMa3p2d%2Beg2x2sJ5%2FuH7KiLJ%2BEUhpHYPIcLmNNiy2yfx5EHx7G%2BhS97mmNKufaIzcWsgISnqlwwG2sRb1nnRWa7fl%2ByLUgx3VxAFsXymfPUhNhSxTUnEbr1shWmYNrGNggEKjS1wyFXCoUL3ULHqGCx8n8UqgiRRkCEPt4DMsGi7jY9LQ4WB7%2BkVr2%2B5IBGsueL694xgsmAzkdooTBkTKkrNqekvO%2FONHreDNG02MJexrh0AmTzXKvHWTlJxcW%2B5XuQtl8BwdO3mdgDQg%2BN07MW63NAxiqNgqdtA9EmOCVO%2FWcjZFmu%2Bu1smrxqGt0elqyFRG4wA4oJ1%2FTqCtvKG4n0e44z%2BolH4jK4ei%2BS1XFtl3hR%2FR6iodTMjX9CGSOy1YFkJ6GD0hj4Pk3ERoodiOCZzR0jzml7%2BNgfpXUnFdeaYWCWnn1W2INSoeiYUSx0Jatj8Jhsj9eusJCQuJQseD0P6WcU7b1jZ3qrk11r%2BT3J7rh77F9DLvKUSt": 371,
        "https://api.1sapp.com/content/getListV2?qdata=RTU4MERCN0EzNDlGMkQxN0U5MEI5NkEzREI2QzJGMkQuY0dGeVlXMGZNVGhsTmpnM00yUXRORGhpTlMwME4yVTFMVGs0TnpZdE1qRmhaV1ptTm1ObFpUazBIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC7SGAC5xqD6WdqxhERT4wbld7fUefUqSBwgzyk7Cd248eXxHzeivEpzcCTVdSE05x09vhkJsV4F1cn69MkpNRmkLim2x5tFNrpgefiFP4b4%2Bsyl9Vc2gzVBXOexyoI%2BT1LJWzFTSWjQxMsRKrYYx1VEzdiHJgds5tIrPp9EexjxAWRXNbWwUFY0dZjVvP6A4HM9KdlFYX4UxrGN37j1CEwmCJtudqI1E36Jn%2Fy7ZAPPPUdGbVwBoy4FzPYut2EDWvZc7lkEiblO2ihWZUdaXjIuuZQbe1TpFC4NZho5J7QgV25J%2BfC5r6bBef8G3gackTroDter6IsFro0ws0xUOYB14RKAN%2BKb99qDChRnkC8kPM0xrjmHCkZaxofDFfnPd24nhrOT97ayl8tK0v7LMOYYMDLtGJmJ0XwfwGzwl3ZpXDjo8uhlNqPEj4YTx7gb7wdis2UMytsuwtfMoQT69FpJklEjHIQQNR84o13cWxGAgKglR9p9P3pNDbsa0W5llLY4er0p1FohOcVAuN32O%2BhhGJ6HtzguT%2F%2B1VNnl3sgafafdXw9jdI2R%2FG6dKfEjpiJo8ALB%2FE%2FjmxfTq4jY7PfPUDQDdc6%2FzkpfZkysvGIhVYHdDrbjPbaTIUFui65kG7Njhk6eRw2dQwgHP1brv%2Fw2ixGevtPUMq7EJ71A2NUaHAsfrGnPBDuQPJFvLZgGwq16ZHWIeoN3T753L9zf49C0smlRjGhUDTH3%2BBBV705Wm1SAlXs8ZgXRbDRMjiMb527reLysbz%2BgXv9ByuJgewdEw2hcQHvWNhH1rE6ckITzFq3jaIHSnzRicfgPttZM4QOEgmJa8DW2n5u1eZ4vunWp7ppCssOJD6bNTYUaB%2F3aygJXU5DcPAahrL4vozgm6uBbLvVkHZyGme29G2sqYQSnqlSS": 84,
    # 历史
        "https://api.1sapp.com/content/getListV2?qdata=QkVGNjFENDM2MEZGMTM0MDU1MDU1RjY1MTk2RTQzRTUuY0dGeVlXMGZOVFF6TW1SbE16Y3RZamd5TUMwME9XWmpMV0ZoWVdRdE56WTJabU14T1dZMk5tRTRIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC4Ej8alAoQCoruvzeasHVgYdd75YV8hjGIGfBCHSgPpQ8hUxqxLU%2BRS8aQhbEIok0IWACtVJ4WvXp0T%2ByOabE0nIoKgf7CYAXxiSVIyk2x%2BUBYeE%2Fb10ASxPqdqFmSD%2FgYcBEBXG4%2BKSGcC4ovf%2BnN2wKyCTPMifU0pMFNDrb%2BQrj%2FdIE7oYglGErgYPOGV0DWv%2FF3PCUuapIhf1nSIE7BNR%2B4Hn7VLjEhuPfhYL2cjf7ST7BSPSga10EdFHYipZwKmYEvJOEPgKhjlYoeYogHvMg3Q2dp66oWlA%2FPE5QzNd8kOYhBj2fhBX1JDP7Vfl6bAs%2BLxM0EOQ0kWJVSx26iYpCAIgBehgAyOsw354kp1RPCaqGjsSqHTBH4gaC6xDfF4sJZT%2FPqPQd68gb8H%2B%2FTdbK%2BYOxlvpGW%2BueS5Ut2vW6kfmS5KMuYHxuhu6Yx5Rr2VEHXVgMWpsGn8Qv98pmOC53RS%2Fg18vRFYj%2FJ8IS7krqhPTE5Y7%2F%2Bdc5CgUzmCufXcw%2FFRwmy0g%2FYelsbHdN8woVRe%2F8oVaZBlDoQ71uUGaxCOSBduY4UbjCT%2Ba6QOjgem8k3hoZPw24ADWqdHTeRZAM3y0ZdB%2FXvCkGK0Dyc06ofPTwNU1xFSOaxfMcLNfLw8UQIBh2Wnq08aX5JWSqy7RCscg05xOU2ldmCUF0%2Fp%2FRb2f9iywnfcUTmsjvglfaHtHiZFO53%2FCCAq8FOHEeqpBP95TozDitk5ES9P9%2F%2FAzb88HM64C633Gr37g78u%2FlmbktrkVzw5uamsY1w5GcWlWlmG5bFuqkA6NOEu5URpfHrFiJuwQRrfHGiiMpMthgNX6JoG2q0NzwuUdyvmTCvQCS9XT%2F6Njnd%2BgU6OyikXOLg0Ht4wDj3y5mFcbojrg%2BpmgzlUVIXkeSAg9XCLvthqu7Gg": 85,
    # 房产
        "https://api.1sapp.com/content/getListV2?qdata=MTFEOUY1OTZENUE0RUU0NjQ5Mzc4RjFFRjA1NTIyODcuY0dGeVlXMGZOMlUxWTJWbE56UXRZVGMzTVMwME1Ua3hMV0kxTkdRdFl6Y3hZMlF3TVRFNVpUSXdIblpsY25OcGIyNGZNVEVlY0d4aGRHWnZjbTBmWVc1a2NtOXBaQjVsWXg4eC5DYwIwzGu8yxkFj1752dvLXufnP1J1RXLeM4MbsG8GSMC4G7Zxo7MsnKawamuVZf5D5E5cYet2zRJm0HZiWcAH%2B%2Br95wEjvzFCBZttyS74j7i3rZRvYKkMrwckO80GMP6JMSEzCQDrOw2ri%2BCzJzpMmg9%2FLGHZLiviCFTDxXAuMN8jnQ01HpJDB5aso5leDN8a56EdBSb%2FVuHTGOZ%2B7j0mH2%2FVKFGPQqiJnqOhUQVxIqXyAXIG7L6BNNSsRrBhQIQjHDNzy3X4RBkAedA%2B6Exp0%2Fhry%2BPIPtArWXWDhBDnxW6IrOLx034K1g%2FijZngXFoM8ptvrvC0rMXCVZRruGlYLuY8QbQ5ruwoGs4QEftKxNYQJEXGmH9weR235hqe8mJSavCjZ65XiECyYKxoUZCjR9%2B5iESGpJa4IpaIC7NHCe17geBRieRtKqyRmFebtNgjsOupCK5SqhRon1Fphcv8VqLNYtouvxIfFuIoAZ7uy4rDHwV%2B5hPirRHHXwh%2BNL7tdwElDy%2FetK0perukOrW0wskEAn2sdRTQ1TiQnONI9%2FFZw97KFOeHUDUMgdL5dUI01E01%2FqSQY%2BRPz7mI49iOlJ2KuglzAs1z3Yw28v77GyhzW0ybwyO7oAxef7ApCbor8GTkip%2BX0SejUHkyyfj7Y%2B4IpJMXUmvZGIqRcdiJWxnR0L4FpqBc1sUJqi1SL%2Bo%2FG9bRq3xp7NiHYCocq%2Fkx0Q8YYKoSMihjNYblK2c%2BkFz%2FVHeK%2FqzF1rMi4tSFP1nL%2F6e%2F9udhBMaMWvjIApZtO0a%2BUvZj32NuuPAwPT6Wdj7A%2Fc%2B89RuwXp3HLc4tH90elkaCe25wTguZ6z5tq5VoIR9bayh1lD1JGG52%2FQw3EZsfxr%2FxuICt%2FNYsgWvwpT583qot%2BG%2B9mOJH0AfBuMeFeKxD": 86,
    # 家居
    }
    
    def parse(self, response):
        rs = json.loads(response.text)
        if rs.get("code") != 0 or not isinstance(rs.get('data'), dict):
            return self.produce_debugitem(response, 'json error')
        
        for i in rs.get('data').get('data'):
            if i.get('type') == 'ad':
                continue  # 排除广告
            if i.get('has_video') != 0:
                continue  # 排除视频
            
            news_url = i.get('detail_url')
            if not news_url:
                self.log('have not detail_url, url=%s' % i.get('url'))

            pubtime = i.get('publish_time')

            title = i.get('title')
            origin_name = i.get('source_name')
            content = i.get('detail')
            if content:
                if i.get('has_article') == 0:
                    
                    content, media = self.img_cont(content)
                else:
                    content, media, _, _ = self.content_clean(content)
                yield self.produce_item(
                    response=response,
                    title=title,
                    pubtime=pubtime,
                    origin_name=origin_name,
                    
                    content=content,
                    media=media,
                    srcLink=i.get('url') or i.get('share_url'),
                )
            else:
                yield Request(
                    url=news_url,
                    callback=self.parse_item,
                    meta={'source_id': response.meta['source_id'], 'title': title, 'pubtime': pubtime,
                           'origin_name': origin_name,
                          'start_url_time': response.meta.get('start_url_time'), 'schedule_time': response.meta.get('schedule_time')}
                )
    
    def img_cont(self, cont_list):
        media = {"images": {}}
        new_content = ''
        for i, j in enumerate(cont_list):
            media["images"][str(i + 1)] = {'src': j.get('image')}
            new_content += '<p>' + '${{%s}}$' % (i + 1) + '</p>'
            if j.get('desc'):
                new_content += '<p>' + j['desc'] + '</p>'
        return new_content, media
    
    def parse_item(self, response):
        rs = json.loads(response.text)
        if not rs.get('detail'):
            return self.produce_debugitem(response, 'json error')
        try:
            content, media, _, _ = self.content_clean(rs.get('detail'))
        except:
            return
        return self.produce_item(
            response=response,
            title=response.meta.get('title'),
            pubtime=response.meta.get('pubtime'),
            origin_name=response.meta.get('origin_name'),
            
            content=content,
            media=media,
        )
