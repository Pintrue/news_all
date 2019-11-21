#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/17 6:33
# @Author  : wjq
# @File    : debug_delay.py


from news_all.db_method import DebugRW, SourceR
from datetime import datetime
import csv

from news_all.tools.database_work import MongoBaseRW, DatabaseConfig
from news_all.tools.others import to_list


def get_delay_time(st, et, env='local', kfk_ok=True):
    all_time = 0
    all_items = 0
    
    nw = DebugRW(env)
    dic = {"crawlTime": {"$gt": st, "$lt": et}}
    res = nw.find(dic)  # dic={"source_id":255}
    
    for i in res:
        it = i.get('delay_time')
        if it and i.get('kfk_ok_time'):
            print(it)
            all_time += it
            all_items += 1
    
    if all_items > 0:
        print('items: %s, delay_time: %s' % (all_items, all_time // all_items))
    else:
        print('no debug news!')


def get_titles(st, et, env='local', source_ids=None):
    """通过新闻标题，验证爬虫爬新闻是否爬全"""
    nw = DebugRW(env)
    dic = {"crawlTime": {"$gt": st, "$lt": et}}
    if isinstance(source_ids, list):
        ss = source_ids
    else:
        ss = [source_ids]
    
    st = {}
    for sid in ss:
        st[sid] = []
        dic.update({'source_id': int(sid)})
        
        res = nw.find(dic)
        for i in res:
            itt = i.get('title')
            if itt:
                st[sid].append(itt)
                # print(itt)
    
    # print(st)  # {source_id: [title1, title2, ...], ...}
    for i, j in st.items():
        print(i, len(j), '\n', '\n'.join(j), '\n\n')


def get_sid_news_count(st, et, env='local', source_ids=None):  # 各个源发kfk新闻的数量
    nw = DebugRW(env)
    dic = {"kfk_ok_time": {"$gt": st, "$lt": et}}
    if isinstance(source_ids, list):
        ss = source_ids
    else:
        ss = [source_ids]
    
    sd = {}
    for c in ss:
        dic.update({'source_id': c})
        co = nw.coll.count_documents(dic)
        sd[c] = co
    
    print(st.strftime('%Y-%m-%d'), 'source_id数量%s' % len(ss))
    print(sd)
    return sd


def get_news_count(st, et, env='local', source_ids=None):  # 所有源发kfk新闻的数量
    nw = DebugRW(env)
    dic = {"kfk_ok_time": {"$gt": st, "$lt": et}}
    
    if source_ids:
        source_ids = to_list(source_ids)
        dic['source_id'] = {"$in": source_ids}
    c = nw.coll.count_documents(dic)
    print(st.strftime('%Y-%m-%d'), c)
    return c


def get_notin_count(catis, env='local'):  # 分类不包含
    nw = SourceR(env)
    lis = [[i] for i in catis]  # [[140300], [18130], [180300],]
    dic = {"categories": {"$nin": lis}}
    # count = nw.coll.find(dic).count()
    # print(count)
    
    c = nw.coll.count_documents(dic)  # 新的api  和  coll.find(dic).count()相同结果
    print(c)


def update_source(priority, source_ids, r_env='test', w_env='online_out'):
    # todo  同步测试库的source到线上, 加priority字段
    reader = SourceR(r_env)
    writer = SourceR(r_env)


class La(MongoBaseRW):
    db_config = DatabaseConfig.News


def get_srcLink(env='online_out'):
    # db.getCollection('news_all_online_debug').find({srcLink: {'$ne': None}}, {srcLink: 1, _id: 0})
    nw = DebugRW(env)
    sr = La('local')
    
    res = nw.coll.find({"srcLink": {'$ne': None}}, {"srcLink": 1, "_id": 0})
    srcLink = set()
    for r in res:
        if r.get('srcLink') not in srcLink:
            srcLink.add(r.get('srcLink'))
            print(r.get('srcLink'))
            sr.insert({'srcLink': r.get('srcLink')})
    nw.close()
    sr.close()
    # with open('srcLink.csv', 'a') as csvFile:
    #     csvWriter = csv.writer(csvFile)
    #     csvWriter.writerow(srcLink)  # todo csv how解决了写None的问题


if __name__ == '__main__':
    diyijuzi = [2862, 2864, 2866, 2867, 2868, 2869, 2870, 2871, 2872, 2873, 2874, 2875, 2876, 2877, 2878, 2880, 2881,
                2882, 2883, 2884, 2885, 2886, 2887, 2888, 2889, 2890, 2891, 2892, 2893, 2894, 2895, 2896, 2897, 2898,
                2899, 2900, 2901, 2902, 2903, 2904]
    
    duanju = [2454, 2602, 2603, 2605, 2607, 2609, 2610, 2613, 2615, 2617, 2620, 2622, 2695, 2700, 2702, 2712, 2718,
              2720, 2722, 2726]
    
    jcmw_all = [646, 648, 651, 654, 774, 856, 857, 1018, 1054, 1055, 1059, 1060, 1061, 1062, 1063, 1064, 1067, 1121,
                1165, 1314, 1333, 1335, 1338, 1448, 1583, 1681, 1683, 1685, 1802, 1856]
    
    dwx = [2816, 2820, 2822, 2824, 2827, 2829, 2833, 2835, 2842, 2843, 2847, 2848, 2850, 2852, 2853, 2854, 2855, 2858,
           2861, 2863, 2865]
    
    liunian = [2426, 2428, 2430, 2432, 2433, 2435, 2437, 2439, 2441, 2443, 2445]
    
    jd_all = [2733, 2734, 2736, 2740, 2744, 2746, 2748, 2751, 2753, 2754, 2756, 2758, 2760, 2762, 2764, 2767, 2769,
              2771, 2774, 2775, 2778, 2780, 2782, 2732, 2806, 2809, 2811, 2812, 2814]
    
    lz13_all = [2414, 2427, 2429, 2431, 2434, 2436, 2438, 2440, 2442, 2444, 2446, 2447, 2448, 2449, 2450, 2451, 2452,
                2453, 2601, 2604, 2606, 2608, 2611, 2612, 2614, 2616, 2619, 2621]
    
    meiwen = [644, 645, 647, 649, 650, 652, 653, 687, 821, 855]
    
    yueduwen_all = [2144, 2146, 2313, 2371, 2372, 2384, 2386, 2388, 2389, 2390, 2391, 2392, 2393, 2394, 2395, 2399,
                    2404, 2406, 2409, 2411, 2412, 2413]
    
    # ------------------------------------------------------------------------------------------------------------------------
    cctv5_app = [2986, 2987, 2988, 2989, 2990, 2991, 2992, 2993, 2994, 2995, 2996, 2997, 2998, 2999, 3000, 3001, 3002,
                 3003, 3004, 3005, 3006, 3007, 3009, 3010, 3011, 3012, 3013, 3014, 3015, 3016]
    
    cankao_app = [3655, 3370, 3371, 3372, 3373, 3374, 3375, 3376, 3377, 3378, 3379, 3380, 3381, 3382, 3383, 3384, 3385,
                  3386, 3387, 3388]
    
    cctvchild_app = [3017, 3018, 3019, 3020, 3021, 3022, 3023, 3024, 3025, 3026, 3027, 3028, 3029, 3030, 3031, 3032,
                     3033, 3034]
    
    gongren_app = [532, 534, 559, 570, 579, 589, 599, 600, 616, 621, 622, 623]
    
    china_news_app = [2959, 2960, 2961, 2962, 2963, 2964, 2965, 2966, 2967, 2968, 2969, 2970, 2971, 2972, 2973, 2974,
                      2975, 2976, 2977,
                      2978, 2979, 2980, 2981, 2982, 2983, 2984, 2985]
    
    china_app = [3046, 3047, 3048, 3049, 3050, 3051, 3052, 3053, 3054, 3055, 3056, 3057, 3058, 3059, 3060, 3061, 3062,
                 3063, 3064, 3065, 3066, 3067, 3068, 3069, 3070, 3071]
    
    chinasearch_app = [3461, 3462, 3463, 3464, 3465, 3466, 3467, 3468, 3469, 3470, 3488, 3489, 3490, 3491, 3494, 3495,
                       3496, 3497, 3498, 3499]
    
    cntvcbox_app = [3316, 3317, 3318, 3319, 3320, 3321, 3322, 3323, 3324, 3325, 3326, 3327, 3328, 3329, 3330, 3331,
                    3332, 3333, 3334, 3335, 3336, 3337, 3338, 3339, 3340, 3341, 3350, 3351, 3352, 3353, 3354, 3355,
                    3356, 3357, 3358, 3359, 3360, 3361, 3362, 3363, 3364, 3365, 3366, 3367, 3368, 3369]
    
    cri_app = [418, 420, 427, 430, 435, 442, 443, 445, 447, 454, 464, 480, 506, 519, 522, 523, 525, 526, 527, 528, 529,
               530, 615]
    
    xinhuanet_app = [2906, 2907, 2908, 2909, 2910, 3656, 3657, 3678, 3679, 3693, 3694, 3695, 3696, 3697, 3698]
    
    guangming_app = [624, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 640, 641]
    
    jcrb_app = [3389, 3391, 3393, 3396, 3397, 3398, 3399, 3394]
    
    jwview_app = [3699, 3700, 3701, 3702, 3703, 3704, 3705, 3706, 3707, 3708, 3709, 3710, 3711, 3712, 3713, 3714, 3715,
                  3716, 3717, 3718, 3719]
    
    policeinter_app = [3456, 3457, 3458, 3459, 3460]

    qingnian_app = [2926, 2927, 2928, 2929, 2930, 2931, 2932, 2933, 2934]

    yscj_app = [390, 396, 407, 410, 412, 414, 423, 428, 434, 437, 444, 446, 448, 456, 508, 515, 520, 521]

    qiushi_app = [3654, 3084, 3085, 3086, 3087, 3090, 3092, 3093, 3094, 3099, 3100, 3101, 3102, 3103]

    zgmtb_app = [2953, 2954, 2955, 2956, 2957, 2958]

    zgsk_app = [391, 392, 393, 394, 395, 397, 409, 411, 413]

    zgyjglb_app = [3072, 3073, 3074, 3075, 3076, 3077, 3078, 3079]

    zqbapp_app = [3720, 3722, 3723, 3724, 3725, 3726, 3727,
     3728, 3729, 3730, 3731, 3732, 3733, 3734,
     3735, 3736, 3737, 3738, 3739, 3740, 3741,
     3742, 3743, 3744, 3745, 3746, 3747, 3754,
     3755, 3756, 3721, 3748, 3749, 3750, 3751, 3752, 3753, ]
    
    zgjw_app = list(range(3401, 3454)) + [3454, 3455]

    sc = get_sid_news_count(st=datetime(2019, 8, 12), et=datetime(2019, 8, 13), env="local", source_ids=zgjw_app)

    total = 0
    for i, j in sc.items():
        if j == 0:
            print(i, '==0')
            continue
        total += j

    print('total=', total)