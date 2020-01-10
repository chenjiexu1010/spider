# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import requests
import json
import re
import time


# work_book = xlrd.open_workbook(u'test.xlsx')
# sheet_name = work_book.sheet_names()
# print(sheet_name)


# work_book = xlwt.Workbook()
# sheet = work_book.add_sheet('Sheet01')
# sheet.write(0, 1, 'test')
# work_book.save(u'test.xls')

'''
    Cookie: _xsrf=Neua2deAGDYjzmsrHsdcinKwnAWFAFI5; 
    _zap=02f3479e-9090-4e55-96c4-f77d78eddf33;
    d_c0="ALBunjhdtQ-PTrYDu3gBJr_jZmNNz6qPH0Y=|1562649179";
    z_c0="2|1:0|10:1562893502|4:z_c0|92:Mi4xWWk4akNBQUFBQUFBc0c2ZU9GMjFEeVlBQUFCZ0FsVk52aW9WWGdCb3ZHZzlfUTBaNXpma2RabzhveFRNMGhsc01B|db459110a648557f52a5007dca5dd0d6c3aed4862e995f53d59b0137fabec546";
    __utmv=51854390.100--|2=registration_date=20180310=1^3=entry_date=20180310=1; tst=r; __utma=51854390.720847714.1564978275.1565582695.1566781022.5; 
    __utmz=51854390.1566781022.5.5.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; 
    q_c1=cd33a8bc836d40a88eb033cd93923761|1576573732000|1563795842000; tgw_l7_route=302fb19f026f5b11b5e883a5cbbb5031;
     Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1576574928,1576659026,1576806285,1576806313; 
    Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1576806316
'''

'''
   https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=6ed822203080ad17e6f2f0fc72679443&desktop=true&page_number=7&limit=6&action=down&after_id=35
   https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=4352f63abb7b1e210ebcd9767a46760e&desktop=true&page_number=2&limit=6&action=down&after_id=5
'''

# 时间戳转换为普通时间
# created_time = 1576811538
# created_time = time.localtime(created_time)
# created_time = time.strftime('%Y-%m-%d %H:%M:%S', created_time)
# print(created_time)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Cookie': 'xsrf=Neua2deAGDYjzmsrHsdcinKwnAWFAFI5; _zap=02f3479e-9090-4e55-96c4-f77d78eddf33; d_c0="ALBunjhdtQ-PTrYDu3gBJr_jZmNNz6qPH0Y=|1562649179"; __utmv=51854390.100--|2=registration_date=20180310=1^3=entry_date=20180310=1; tst=r; __utma=51854390.720847714.1564978275.1565582695.1566781022.5; __utmz=51854390.1566781022.5.5.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; q_c1=cd33a8bc836d40a88eb033cd93923761|1576573732000|1563795842000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1576574928,1576659026,1576806285,1576806313; l_n_c=1; r_cap_id="ZjFhNTY0NzAxYmJkNGUxNDg1MTYwMzAyNDRkNTExN2I=|1576807058|57e838eeeb319c03344f95375b86c6c4cf298398"; cap_id="MGViODFjMGE5OGNiNDFkNWE1NjEwOThmMTEyMmYwZTc=|1576807058|6414f55a32b20f6032a7cbb12ca548d186e6c42c"; l_cap_id="OGJlYmM2N2Y3YTNiNGNkMzlkODcwMzJhYzM4YjZiMGM=|1576807058|1421871f49f93322327ddbdd5d9dedba358dcf71"; n_c=1; capsion_ticket="2|1:0|10:1576807090|14:capsion_ticket|44:NjBhMzNkMzkzNDY3NGEyOTljMjE5YzVmZjNkYjYxYTA=|eff3ab2eb824a4b786ce090f56bb628a141953732d969f23793ede41a9fb2e23"; z_c0=Mi4xWWk4akNBQUFBQUFBc0c2ZU9GMjFEeGNBQUFCaEFsVk41M2pwWGdEc2UxaFVRT1dPSlBmdElFTFpKSjZDSjcxdmxn|1576807143|f4055ee358c162fa02696194633aefc1b3b44ac3; tgw_l7_route=66cb16bc7f45da64562a077714739c11; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1576810043',
    'Referer': 'https://www.zhihu.com/',
    'X-Ab-Param': 'zr_km_style=base;zr_paid_answer_exp=0;se_aa_base=0;se_famous=1;soc_zcfw_shipinshiti=0;zr_paid_answer_merge=50;se_subtext=1;tp_club_qa=1;soc_wonderuser_recom=2;pf_noti_entry_num=0;se_ltr_dnn_cp=0;se_college=default;se_time_threshold=0;tsp_redirecthotlist=2;zr_km_category=open;se_zu_recommend=0;li_paid_answer_exp=0;ug_fw_answ_aut_1=0;zw_sameq_sorce=999;zr_km_feed_rerank=0;se_mobileweb=1;ug_newtag=1;se_ios_spb309=1;tp_meta_card=0;se_likebutton=0;se_col_boost=1;se_preset_tech=0;soc_zcfw_broadcast2=1;zr_km_special=open;zr_article_new=close;se_entity_model_14=0;se_expired_ob=0;zr_des_detail=1;se_ab=0;se_auto_syn=0;se_cardrank_4=1;li_tjys_ec_ab=0;zr_art_rec=base;zr_esmm_model=old;se_featured=1;top_v_album=1;ug_follow_answerer=0;tp_topic_rec=0;tsp_vote=2;li_cln_vl=no;zr_esmm_model_mix=model_17;se_webmajorob=0;se_topiclabel=1;se_senet=0;tp_topic_head=0;pf_creator_card=1;zr_video_rank_nn=new_rank;se_whitelist=1;se_perf=0;se_multi_task_new=0;zr_km_recall_num=open;se_adxtest=1;zr_slot_cold_start=aver;zr_prerank_heatscore=true;se_cardrank_3=1;li_android_vip=0;li_purchase_test=0;li_qa_new_cover=1;qap_question_author=0;top_ydyq=X;zr_paid_answer_mix=mixed_13;se_pek_test=0;top_new_feed=5;top_root=0;se_waterfall=0;soc_yxzl_zcfw=0;se_hotmore=2;se_preset_label=0;se_sug=1;tp_score_1=a;zr_km_item_cf=open;se_college_cm=1;ls_fmp4=0;qap_payc_invite=0;se_dnn_unbias=1;se_member_rescore=0;tp_club_pk=1;se_cardrank_2=1;soc_ri_merge=0;li_qc_pt=0;li_de=no;zr_km_feed_nlp=old;zr_video_recall=current_recall;se_agency= 0;tp_m_intro_re_topic=1;top_universalebook=1;li_pay_banner_type=6;li_answer_card=0;se_pek_test2=0;soc_stickypush=0;se_p_slideshow=1;ug_goodcomment_0=1;li_vip_lr=1;se_ltr_cp_new=0;soc_special=0;li_qa_cover=old;li_salt_hot=1;zr_item_nn_recall=close;ls_videoad=2;li_query_match=0;se_cate=1;tp_sticky_android=2;soc_zuichangfangwen=0;se_rel_search=1;se_payconsult=5;ls_bullet_guide=0;zr_km_recall=default;zr_intervene=0;se_ctx=0;se_wannasearch=a;qap_ques_invite=0;soc_leave_recommend=2;se_movietab=1;ls_zvideo_license=1;zr_se_new_xgb=0;se_webtimebox=1;top_test_4_liguangyi=1;ug_zero_follow_0=0;se_new_merger=1;soc_bignew=1;soc_update=0;tp_sft=a;qap_thanks=1;se_webrs=1;se_new_topic=0;se_ad_index=10;ls_zvideo_trans=0;pf_foltopic_usernum=50;zr_recall_heatscore=4_6;se_multianswer=0;tp_qa_toast=1;tp_qa_metacard_top=top;ls_zvideo_rec=2;li_album_liutongab=0;li_qa_ad_card=0;li_sku_bottom_bar_re=0;zr_km_answer=open_cvr;li_se_across=0;zr_km_item_prerank=old;zr_km_prerank=new;zw_payc_qaedit=0;tp_club_qa_pic=1;li_se_heat=1;li_se_section=1;zr_rewrite_query=1;se_club_post=5;top_ebook=0;top_native_answer=9;se_cardrank_1=0;se_lottery=0;soc_brdcst3=0;se_entity_model=1;se_amovietab=1;tp_header_style=1;zr_slotpaidexp=5;top_quality=0;pf_newguide_vertical=0;zr_video_rank=new_rank;se_websearch=3;tp_topic_entry=0;tp_topic_style=0;li_video_section=0;tp_qa_metacard=1;zr_answer_rec_cp=open;se_backsearch=0;li_qa_btn_text=0;li_ebook_audio=0;zr_km_slot_style=event_card;zr_test_aa1=1;qap_question_visitor= 0;se_topicfeed=0;ug_follow_answerer_0=0;se_zu_onebox=0;ls_zvideo_like=2;li_vip_no_ad_mon=0;zr_expslotpaid=1;zr_km_topic_zann=new;se_pek_test3=0;tsp_hotlist_ui=9;li_hot_score_ab=0;zr_km_sku_mix=sku_50;zr_infinity_member=close;zr_book_chap=1;tp_club_header=1;se_search_feed=N;soc_zcfw_badcase=0;pf_fuceng=1;zr_km_feed_prerank=new;se_spb309=0;se_timebox_up=0;se_hotsearch=1;ug_zero_follow=0;se_colorfultab=1;tp_topic_tab=0;soc_zcfw_broadcast=0;top_hotcommerce=1;li_se_media_icon=1;se_site_onebox=0;zr_ans_rec=gbrank;zr_rec_answer_cp=close;ug_follow_topic_1=2;se_use_zitem=0;se_ctr=0;tp_sft_v2=d;zr_rel_search=base;soc_bigone=1;soc_notification=1;soc_authormore=2;sem_up_growth=in_app;zr_new_commodity=1;se_billboardsearch=0;se_hot_timebox=1',
    'X-API-VERSION': '3.0.53',
    'Connection': 'keep-alive',
}
url = 'https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=243d8893693ef2abf06143131fe55971&desktop=true&page_number=1&limit=6&action=down&after_id=29'

request = requests.get(url=url, headers=headers)
# cookie = request.cookies
# print(cookie)
if request.status_code == 200:
    zhihu_content = request.json()['data']
    for article in zhihu_content:
        if 'target' in article.keys():
            # print(article.keys())
            print('标题: %s ,内容: %s' % (article['target']['author']['headline'], article['target']['content']))
