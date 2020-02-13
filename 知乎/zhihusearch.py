# -*- coding:utf-8 -*-
# !/usr/bin/Python3
import requests
import json
import random
from flask import Flask
from requests.auth import HTTPProxyAuth

host = '192.168.2.74'
app = Flask(__name__)


class ZhiHuSearch(object):
    def __init__(self):
        self.account_info = []
        ZhiHuSearch.read_account(self)
        self.request_url = ''
        self.auth = HTTPProxyAuth('jeqee', 'jeqeeproxy')
        self.next_url = ''

    def read_account(self):
        with open('zhihuaccount.txt', 'r') as r:
            read_list = r.read().splitlines()
            for account in read_list:
                cookies = requests.utils.cookiejar_from_dict(json.loads(str(account.split('\t')[1])), cookiejar=None,
                                                             overwrite=None)
                self.account_info.append(cookies)

    def search_data(self, keyword, t="general"):  # general = 综合 people = 用户
        try:
            url = f'https://www.zhihu.com/api/v4/search_v3?q={keyword}&t={t}&lc_idx=0&correction=1&offset=0&advert_count=0&limit=20&magi=true&is_real_time=0&show_all_topics=0&red_packet=0'
            headers = {
                'Accept': '*/*',
                'x-requested-with': 'fetch',
                'x-app-za': 'OS=iOS&Release=10.3.3&Model=iPhone8,1&VersionName=6.23.0&VersionCode=1674&Width=750&Height=1334&DeviceType=Phone&Brand=Apple&OperatorType=46011',
                'x-hybrid': '1',
                'Accept-Language': 'zh-cn',
                'Accept-Encoding': 'gzip, deflate',
                'x-api-version': '3.0.91',
                'x-network-type': 'WiFi',
                'User-Agent': 'ZhihuHybrid osee2unifiedRelease/1674 osee2unifiedReleaseVersion/6.23.0 Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60',
                'X-Ab-Param': 'soc_zcfw_broadcast2=1;soc_bigone=1;zr_new_commodity=1;top_v_album=1;li_paid_answer_exp=0;ug_goodcomment_0=1;se_zu_recommend=0;soc_notification=1;se_new_merger=1;se_cardrank_1=0;tp_qa_metacard_top=top;tp_qa_toast=1;tp_topic_entry=0;li_album_liutongab=0;zr_ans_rec=gbrank;se_ab=0;top_test_4_liguangyi=1;ug_follow_answerer_0=0;se_preset_label=1;se_cardrank_4=1;zr_video_rank=new_rank;se_cp2=0;se_senet=0;li_cln_vl=no;se_cardrank_3=1;se_lottery=0;tp_sft_v2=d;top_root=0;se_webtimebox=1;se_sug=1;se_wannasearch=a;tp_m_intro_re_topic=1;se_zu_onebox=0;ug_zero_follow_0=0;qap_thanks=1;zr_search_satisfied=1;se_entity_model_14=0;zr_slot_training=1;zr_test_aa1=1;top_hotcommerce=1;se_dnn_unbias=1;zr_km_sku_mix=sku_55;se_expired_ob=0;zr_rec_answer_cp=open;se_pek_test=1;tp_topic_style=0;tp_topic_tab=0;ls_fmp4=0;qap_question_author=0;soc_stickypush=0;se_perf=0;soc_leave_recommend=2;qap_payc_invite=0;se_related_index=3;se_mobileweb=1;top_new_feed=5;ls_zvideo_license=1;zr_article_new=open;se_webmajorob=0;se_spb309=0;ls_zvideo_rec=2;qap_ques_invite=0;soc_zcfw_badcase=0;se_whitelist=1;soc_zuichangfangwen=0;se_auto_syn=0;tp_topic_head=0;zr_km_answer=open_cvr;zr_paid_answer_exp=0;top_quality=0;li_sc=no;tp_topic_rec=2;ug_follow_topic_1=2;se_p_slideshow=1;pf_fuceng=1;se_hotsearch=0;se_use_zitem=0;li_se_section=1;zr_km_slot_style=event_card;se_pek_test2=1;zr_km_sku_thres=false;se_pek_test3=1;tp_qa_metacard=1;soc_zcfw_shipinshiti=0;pf_newguide_vertical=0;ug_newtag=1;se_search_feed=N;se_websearch=3;se_ltr_dnn_cp=0;se_col_boost=1;se_agency= 0;li_vip_lr=1;zr_des_detail=0;ug_fw_answ_aut_1=0;ls_zvideo_like=2;ls_zvideo_trans=0;top_ydyq=X;se_time_threshold=0;li_hot_score_ab=0;zr_km_style=base;li_vip_no_ad_mon=0;zr_book_chap=1;se_college_cm=1;se_topicfeed=1;se_adxtest=1;se_webrs=1;soc_brdcst3=0;li_qa_btn_text=0;zr_slot_cold_start=aver;li_qc_pt=0;tp_header_style=1;zw_payc_qaedit=0;se_college=default;tp_club_join=0;pf_noti_entry_num=0;sem_up_growth=in_app;se_backsearch=0;li_se_across=1;soc_special=0;zr_expslotpaid=3;tp_club_tab=0;soc_wonderuser_recom=2;soc_ri_merge=0;se_movietab=1;tp_club_header=1;soc_zcfw_broadcast=0;se_ad_index=10;li_se_media_icon=1;li_tjys_ec_ab=0;li_sku_bottom_bar_re=0;se_entity_model=1;top_ebook=0;ug_follow_answerer=0;se_sug_entrance=0;soc_bignew=1;se_rel_search=1;soc_update=0;ls_videoad=2;zr_km_feed_nlp=old;qap_question_visitor= 0;zr_video_rank_nn=new_rank;se_hotmore=2;se_colorfultab=1;li_de=yes;tp_club_qa=1;se_new_topic=0;se_topiclabel=1;se_site_onebox=0;li_pay_banner_type=6;zr_slotpaidexp=1;se_billboardsearch=0;se_amovietab=1;li_ebook_audio=0;se_ltr_cp_new=0;tp_sft=a;se_waterfall=0;se_multi_task_new=2;se_preset_tech=0;tp_meta_card=0;li_salt_hot=1;se_cardrank_2=1;se_timebox_up=0;se_featured=1;pf_creator_card=1;zr_se_new_xgb=0;tp_club_pk=1;li_purchase_test=0;li_video_section=0;tp_score_1=a;soc_yxzl_zcfw=0;top_universalebook=1;se_likebutton=0;se_club_post=5;se_multianswer=0;tsp_vote=2;li_answer_card=0;li_se_heat=1;zr_rewrite_query=1;zr_intervene=0;zr_rel_search=base;se_member_rescore=0;tp_club_android_join=0;li_qa_cover=old;se_subtext=1;zr_answer_rec_cp=open;zr_video_recall=current_recall;se_hot_timebox=1;tp_club_qa_pic=1;li_android_vip=0;zw_sameq_sorce=999;se_payconsult=5;soc_authormore=2;tsp_hotlist_ui=7;ug_zero_follow=0;se_ios_spb309=1;se_famous=1;pf_foltopic_usernum=50;tsp_redirecthotlist=5;tp_sticky_android=2;li_qa_new_cover=1;soc_cardheight=0;soc_newfeed=1;li_query_match=0;zr_art_rec=base;se_aa_base=0',
                'x-ad': 'canvas_version:v=4.1;setting:cad=0',
                'Referer': 'https://www.zhihu.com/appview/search/general?magi=1&showHorizonTab=1',
                'x-app-version': '6.23.0',
                'x-udid': 'ACAr3sykohBLBQFRlJViysAp_JK_j00MAXs=',
                'authorization': 'Bearer gt2.0AAAAABgbTPcQoqTM3isgAAAAAAtNVQJgAgB-33s8jifj0M4UZzAuY1WthCfJyA==',
                # 'cookie': '_xsrf=wIvaowxYMdoJvNl72SM21UnlyT20c40b; tgw_l7_route=79c5a098af080bf343c0c50ae917961f; KLBRSID=57358d62405ef24305120316801fd92a|1578572750|1578572747; z_c0=gt2.0AAAAABgbTPcQoqTM3isgAAAAAAtNVQJgAgB-33s8jifj0M4UZzAuY1WthCfJyA==; zst_82=2.0ANAVHtCkohALAAAASwUAADIuMMsbF14AAAAAu4twqU77IM-OteXSqKMd9l2V80c=; capsion_ticket="2|1:0|10:1578572750|14:capsion_ticket|44:ZTMzMjk3N2FlMTBmNGRmOTk0NjIyNmUzYjQ2N2IyNDk=|22542841f7aadf406c6569ac73d51f78fa280fa61c2e14cb502369eeb82cb10c"',
                'x-suger': 'SURGVj0yNzBCRUMyOC0zMkRCLTExRUEtQTcyQy1GMjE4OTg2OUYwN0I7SURGQT0yNzBCRTkxQy0zMkRCLTExRUEtQTcyQy1GMjE4OTg2OUYwN0I7VURJRD1BQ0FyM3N5a29oQkxCUUZSbEpWaXlzQXBfSktfajAwTUFYcz0=',
                'X-ZST-82': '2.0ANAVHtCkohALAAAASwUAADIuMMsbF14AAAAAu4twqU77IM-OteXSqKMd9l2V80c='
            }
            ip = ZhiHuSearch.get_proxy_ip(self)
            if not ip:
                return '代理获取失败'
            s = requests.session()
            s.cookies = self.account_info[random.randint(0, len(self.account_info))]
            resp = s.get(url, proxies={'http': ip}, headers=headers, auth=self.auth, verify=False)
            resp.encoding = 'utf-8'
            if resp.status_code != 200:
                return '知乎:请求状态码:$s' % resp.status_code
            tex = json.loads(resp.text)
            handle_list = ZhiHuSearch.dict_handle(self, tex)
            self.next_url = tex['paging']['next']
            while True:
                if not self.next_url:
                    break
                if len(handle_list) >= 20:
                    break
                else:
                    # 查找下一页
                    next_handle_list = ZhiHuSearch.next_search(self, self.next_url, headers)
                    if not next_handle_list:
                        break
                    for article in next_handle_list:
                        if len(handle_list) >= 20:
                            break
                        else:
                            handle_list.append(article)
            return handle_list
        except Exception as e:
            print(e)

    def next_search(self, url, headers):
        try:
            resp = requests.get(url, headers=headers, verify=False)
            resp.encoding = 'utf-8'
            tex = json.loads(resp.text)
            self.next_url = tex['paging']['next']
            handle_list = ZhiHuSearch.dict_handle(self, tex)
            return handle_list
        except Exception as e:
            print(e)
        return ''

    # 请求返回值处理
    def dict_handle(self, article_dic):
        handle_list = []
        try:
            for article in article_dic['data']:
                # 排除不是搜索结果
                if article['type'] != 'search_result':
                    continue
                article_object = article['object']
                if 'author' in dict(article_object).keys():
                    question_id = ''
                    if 'question' in dict(article_object).keys():
                        question_id = article['object']['question']['id']
                    obj = {'ArticleTitle': article['highlight']['title'].replace('<em>', '').replace('</em>', ''),
                           'ArticleUrl': article['object']['url'],
                           'QuestionId': question_id,
                           'QuestionContent': article['object']['excerpt'],
                           'QuestionUrl': article['object']['author']['url'],
                           'QuestionAccount': article['object']['author']['name'],
                           'ArticleId': article['object']['id']}
                    handle_list.append(obj)
        except Exception as e:
            print(e)
        return handle_list

    # 获取代理Ip
    def get_proxy_ip(self):
        ip = ''
        try:
            proxy_result = requests.get('http://192.168.2.74:25003/api/GetRandomProxy')
            if proxy_result.status_code == 200:
                info = json.loads(proxy_result.content.decode('utf-8'))
                ip = info['_ProxyAddress']
        except Exception as e:
            pass
        return ip


# 实例化类
zhihu = ZhiHuSearch()


@app.route('/zhihusearch/<keyword>')
def zhihu_search_interface(keyword):
    articles = zhihu.search_data(keyword)
    if articles:
        return json.dumps(articles, ensure_ascii=False)
    else:
        return '返回数据为空'


if __name__ == '__main__':
    app.run(host=host, port=25025, debug=True)
    # zhihu = ZhiHuSearch()
    # zhihu.search_data('脂肪填充')
