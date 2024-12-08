import random
import datetime
import hashlib


def generate_message():
    final_str = ''
    for i in range(random.randint(1, 15)):
        integer = random.randint(1, 100000)
        string = hashlib.md5(int(integer).to_bytes(8, 'big', signed=True)).hexdigest()
        string = string[:random.randint(1, 15)]
        final_str += string + ' '
    return final_str


def clear_calls(d):
    d.shell(f"su -c /data/local/sqlite3 /data/data/com.samsung.android.providers.contacts/databases/calllog.db \"\\\"delete from calls;\\\"\"")


def clear_sms(d):
    f = d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"drop table canonical_addresses;\\\"\"")
    print(f)
    query = """CREATE TABLE canonical_addresses (_id INTEGER PRIMARY KEY AUTOINCREMENT,address TEXT);"""
    f = d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"{query}\\\"\"")
    print(f)
    f = d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"drop table threads;\\\"\"")
    print(f)
    query = """CREATE TABLE threads (_id INTEGER PRIMARY KEY AUTOINCREMENT,date INTEGER DEFAULT 0,message_count INTEGER DEFAULT 0,recipient_ids TEXT,snippet TEXT,snippet_cs INTEGER DEFAULT 0,read INTEGER DEFAULT 1,archived INTEGER DEFAULT 0,type INTEGER DEFAULT 0,error INTEGER DEFAULT 0,has_attachment INTEGER DEFAULT 0,unread_count INTEGER DEFAULT 0,alert_expired INTEGER DEFAULT 1,reply_all INTEGER DEFAULT -1,group_snippet TEXT,message_type INTEGER DEFAULT 0,display_recipient_ids TEXT,translate_mode TEXT default 'off',secret_mode INTEGER DEFAULT 0,safe_message INTEGER DEFAULT 0,classification INTEGER DEFAULT 0,is_mute INTEGER DEFAULT 0,chat_type INTEGER DEFAULT 0,pa_uuid TEXT,pa_thread INTEGER DEFAULT 0,menustring TEXT,pin_to_top INTEGER DEFAULT -1,using_mode INTEGER DEFAULT 0,from_address TEXT,message_date INTEGER,pa_ownnumber TEXT,snippet_type INTEGER,bin_status INTEGER DEFAULT 0);
CREATE INDEX threadsIndex1 ON threads (date);"""
    f = d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"{query}\\\"\"")
    print(f)
    f = d.shell(
        f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"drop table sms;\\\"\"")
    print(f)
    query = """CREATE TABLE sms (_id INTEGER PRIMARY KEY AUTOINCREMENT,thread_id INTEGER,address TEXT,person INTEGER,date INTEGER,date_sent INTEGER DEFAULT 0,protocol INTEGER,read INTEGER DEFAULT 0,status INTEGER DEFAULT -1,type INTEGER,reply_path_present INTEGER,subject TEXT,body TEXT,service_center TEXT,locked INTEGER DEFAULT 0,error_code INTEGER DEFAULT -1,sub_id  INTEGER DEFAULT -1, creator TEXT,seen INTEGER DEFAULT 0,deletable INTEGER DEFAULT 0,sim_slot INTEGER DEFAULT 0,sim_imsi TEXT,hidden INTEGER DEFAULT 0,group_id INTEGER,group_type INTEGER,delivery_date INTEGER,app_id INTEGER DEFAULT 0,msg_id INTEGER DEFAULT 0,callback_number TEXT,reserved INTEGER DEFAULT 0,pri INTEGER DEFAULT 0,teleservice_id INTEGER DEFAULT 0,link_url TEXT,svc_cmd INTEGER DEFAULT 0,svc_cmd_content TEXT,roam_pending INTEGER DEFAULT 0,spam_report INTEGER DEFAULT 0,secret_mode INTEGER DEFAULT 0,safe_message INTEGER DEFAULT 0,favorite INTEGER DEFAULT 0,d_rpt_cnt INTEGER DEFAULT 0,using_mode INTEGER DEFAULT 0,from_address TEXT,announcements_subtype INTEGER DEFAULT 0,announcements_scenario_id TEXT,device_name TEXT,correlation_tag TEXT,object_id TEXT,cmc_prop TEXT,bin_info INTEGER DEFAULT 0,re_original_body TEXT,re_body TEXT,re_original_key TEXT,re_recipient_address TEXT,re_content_uri TEXT,re_content_type TEXT,re_file_name TEXT,re_type INTEGER DEFAULT 0,re_count_info TEXT);
CREATE TRIGGER sms_update_thread_on_insert AFTER INSERT ON sms BEGIN  UPDATE threads SET    date = new.date,     snippet = substr(new.body,1,300),     snippet_cs = 0,    snippet_type = new.type  WHERE threads._id = new.thread_id  AND (new.reserved = 0 OR (new.reserved = 1 AND new.type = 3));   UPDATE threads SET date = NULL        WHERE (threads._id = new.thread_id)           AND new.reserved > 0           AND 1 = (SELECT COUNT(sms._id) FROM sms WHERE thread_id = new.thread_id)           AND 0 = (SELECT COUNT(wpm._id) FROM wpm WHERE thread_id = new.thread_id)           AND 0 = (SELECT COUNT(pdu._id) FROM pdu WHERE thread_id = new.thread_id AND (m_type=132 OR m_type=130 OR m_type=128));   UPDATE threads SET message_count =      (SELECT COUNT(sms._id) FROM sms LEFT JOIN threads       ON threads._id = thread_id      WHERE thread_id = new.thread_id        AND sms.type != 3) +      (SELECT COUNT(wpm._id) FROM wpm LEFT JOIN threads       ON threads._id = thread_id      WHERE thread_id = new.thread_id      ) +      (SELECT COUNT(pdu._id) FROM pdu LEFT JOIN threads       ON threads._id = thread_id      WHERE thread_id = new.thread_id        AND (m_type=132 OR m_type=130 OR m_type=128)        AND msg_box != 3) , unread_count =        (SELECT count(*) FROM sms LEFT JOIN threads        ON threads._id = thread_id       WHERE thread_id = new.thread_id       AND sms.read = 0 AND sms.type = 1) +        (SELECT count(*) FROM wpm LEFT JOIN threads        ON threads._id = thread_id       WHERE thread_id = new.thread_id       AND wpm.read = 0 ) +        (SELECT count(*) FROM pdu LEFT JOIN threads        ON threads._id = thread_id       WHERE thread_id = new.thread_id        AND pdu.read = 0        AND (m_type = 128 OR m_type = 132 OR m_type = 130)       AND msg_box = 1)        WHERE threads._id = new.thread_id;   UPDATE threads SET read =     CASE (SELECT COUNT(*)          FROM sms          WHERE read = 0            AND thread_id = threads._id)      WHEN 0 THEN 1      ELSE 0    END  WHERE threads._id = new.thread_id; END;
CREATE TRIGGER sms_update_thread_date_on_update AFTER  UPDATE OF body, date  ON sms BEGIN  UPDATE threads SET    date = new.date,     snippet = substr(new.body,1,300),     snippet_cs = 0,    snippet_type = new.type  WHERE threads._id = new.thread_id; END;
CREATE TRIGGER update_bin_status_on_insert_sms AFTER INSERT ON sms FOR EACH ROW BEGIN  UPDATE threads SET bin_status = 2 WHERE _id = NEW.thread_id AND bin_status = 1; UPDATE im_threads SET bin_status = 2 WHERE normal_thread_id = NEW.thread_id AND bin_status = 1; END;
CREATE TRIGGER sms_update_thread_type_on_update AFTER  UPDATE OF type  ON sms BEGIN  UPDATE threads SET message_count =      (SELECT COUNT(sms._id) FROM sms LEFT JOIN threads       ON threads._id = thread_id      WHERE thread_id = new.thread_id        AND sms.type != 3) +      (SELECT COUNT(wpm._id) FROM wpm LEFT JOIN threads       ON threads._id = thread_id      WHERE thread_id = new.thread_id      ) +      (SELECT COUNT(pdu._id) FROM pdu LEFT JOIN threads       ON threads._id = thread_id      WHERE thread_id = new.thread_id        AND (m_type=132 OR m_type=130 OR m_type=128)        AND msg_box != 3) , unread_count =        (SELECT count(*) FROM sms LEFT JOIN threads        ON threads._id = thread_id       WHERE thread_id = new.thread_id       AND sms.read = 0 AND sms.type = 1) +        (SELECT count(*) FROM wpm LEFT JOIN threads        ON threads._id = thread_id       WHERE thread_id = new.thread_id       AND wpm.read = 0 ) +        (SELECT count(*) FROM pdu LEFT JOIN threads        ON threads._id = thread_id       WHERE thread_id = new.thread_id        AND pdu.read = 0        AND (m_type = 128 OR m_type = 132 OR m_type = 130)       AND msg_box = 1)        WHERE threads._id = new.thread_id;   UPDATE threads SET read =     CASE (SELECT COUNT(*)          FROM sms          WHERE read = 0            AND thread_id = threads._id)      WHEN 0 THEN 1      ELSE 0    END  WHERE threads._id = new.thread_id;   UPDATE threads SET snippet_type = (    SELECT snippet_type FROM (      SELECT date * 1000 AS date, msg_box AS snippet_type, thread_id FROM pdu WHERE thread_id = new.thread_id      UNION       SELECT date, type AS snippet_type, thread_id FROM sms WHERE thread_id = new.thread_id)    ORDER BY date DESC LIMIT 1)  WHERE threads._id = new.thread_id; END;
CREATE TRIGGER sms_update_thread_read_on_update AFTER  UPDATE OF read  ON sms BEGIN   UPDATE threads SET read =     CASE (SELECT COUNT(*)          FROM sms          WHERE read = 0            AND thread_id = threads._id)      WHEN 0 THEN 1      ELSE 0    END  WHERE threads._id = new.thread_id;    UPDATE threads SET unread_count =        (SELECT count(*) FROM sms LEFT JOIN threads        ON threads._id = thread_id       WHERE thread_id = new.thread_id           AND sms.read = 0 AND sms.type = 1) +        (SELECT count(*) FROM wpm LEFT JOIN threads        ON threads._id = thread_id       WHERE thread_id = new.thread_id           AND wpm.read = 0) +        (SELECT count(*) FROM pdu LEFT JOIN threads        ON threads._id = thread_id       WHERE thread_id = new.thread_id            AND pdu.read = 0            AND (m_type = 128 OR m_type = 132 OR m_type = 130)           AND msg_box = 1)   WHERE threads._id = new.thread_id; END;
CREATE TRIGGER update_threads_error_on_update_sms   AFTER UPDATE OF type ON sms  WHEN (OLD.type != 5 AND NEW.type = 5)    OR (OLD.type = 5 AND NEW.type != 5) BEGIN   UPDATE threads SET error =     CASE      WHEN NEW.type = 5 THEN error + 1      ELSE error - 1    END   WHERE _id = NEW.thread_id; END;
CREATE TRIGGER update_threads_message_type_on_update_sms   AFTER UPDATE OF type ON sms  WHEN OLD.type != NEW.type BEGIN UPDATE threads set message_type =  (SELECT    CASE    WHEN type = 'sms' THEN        CASE            WHEN box_type = 3 THEN 1           WHEN box_type = 4 THEN 10           WHEN box_type = 6 THEN 11           WHEN box_type = 5 THEN 3           ELSE 0       END    WHEN type = 'mms' THEN        CASE            WHEN box_type = 3 THEN 1           WHEN box_type = 4 THEN                CASE                    WHEN err_type >= 10 THEN 3                   ELSE 21               END            ELSE 0       END    END FROM (SELECT date *1000 AS date, msg_box AS box_type, err_type, 'mms' AS type, thread_id FROM pdu, pending_msgs    WHERE pdu._id = NEW._id AND pdu._id = pending_msgs.msg_id    UNION SELECT date, type AS box_type, -1 AS err_type, 'sms' AS type, thread_id FROM sms WHERE group_id IS NULL AND thread_id=new.thread_id AND reserved = 0    UNION SELECT date,  group_type AS box_type, -1 AS err_type, 'sms' AS type, thread_id FROM sms WHERE _id=group_id AND thread_id=new.thread_id AND reserved = 0 ORDER BY date DESC LIMIT 1))  WHERE _id = NEW.thread_id; END;
CREATE TRIGGER update_threads_message_type_on_insert_sms   AFTER INSERT ON sms  WHEN NEW.type >= 0 BEGIN UPDATE threads set message_type =  (SELECT    CASE    WHEN type = 'sms' THEN        CASE            WHEN box_type = 3 THEN 1           WHEN box_type = 4 THEN 10           WHEN box_type = 6 THEN 11           WHEN box_type = 5 THEN 3           ELSE 0       END    WHEN type = 'mms' THEN        CASE            WHEN box_type = 3 THEN 1           WHEN box_type = 4 THEN                CASE                    WHEN err_type >= 10 THEN 3                   ELSE 21               END            ELSE 0       END    END FROM (SELECT date *1000 AS date, msg_box AS box_type, err_type, 'mms' AS type, thread_id FROM pdu, pending_msgs    WHERE pdu._id = NEW._id AND pdu._id = pending_msgs.msg_id    UNION SELECT date, type AS box_type, -1 AS err_type, 'sms' AS type, thread_id FROM sms WHERE group_id IS NULL AND thread_id=new.thread_id AND reserved = 0    UNION SELECT date,  group_type AS box_type, -1 AS err_type, 'sms' AS type, thread_id FROM sms WHERE _id=group_id AND thread_id=new.thread_id AND reserved = 0 ORDER BY date DESC LIMIT 1))  WHERE _id = NEW.thread_id; END;
CREATE TRIGGER update_threads_message_type_on_delete_sms   AFTER DELETE ON sms  WHEN OLD.type >= 0 BEGIN UPDATE threads set message_type =  (SELECT    CASE    WHEN type = 'sms' THEN        CASE            WHEN box_type = 3 THEN 1           WHEN box_type = 4 THEN 10           WHEN box_type = 6 THEN 11           WHEN box_type = 5 THEN 3           ELSE 0       END    WHEN type = 'mms' THEN        CASE            WHEN box_type = 3 THEN 1           WHEN box_type = 4 THEN                CASE                    WHEN err_type >= 10 THEN 3                   ELSE 21               END            ELSE 0       END    END FROM (SELECT date *1000 AS date, msg_box AS box_type, err_type, 'mms' AS type, thread_id FROM pdu    LEFT OUTER JOIN pending_msgs ON pdu._id = pending_msgs.msg_id WHERE thread_id = old.thread_id AND reserved = 0    UNION SELECT date, type AS box_type, -1 AS err_type, 'sms' AS type, thread_id FROM sms WHERE group_id IS NULL AND thread_id=old.thread_id AND reserved = 0    UNION SELECT date,  group_type AS box_type, -1 AS err_type, 'sms' AS type, thread_id FROM sms WHERE _id=group_id AND thread_id=old.thread_id AND reserved = 0 ORDER BY date DESC LIMIT 1))  WHERE _id = OLD.thread_id; END;
CREATE TRIGGER Cmas_cleanup DELETE ON sms BEGIN   DELETE FROM cmas  WHERE sms_id=old._id;END;
CREATE TRIGGER sms_words_update AFTER UPDATE OF [body] ON sms BEGIN UPDATE words  SET index_text = NEW.body WHERE (source_id=NEW._id AND table_to_use=1);  END;
CREATE TRIGGER sms_words_delete AFTER DELETE ON sms BEGIN DELETE FROM   words WHERE source_id = OLD._id AND table_to_use = 1; END;
CREATE TRIGGER sms_update_thread_safe_message_on_insert AFTER INSERT ON sms BEGIN  UPDATE threads SET    safe_message = new.safe_message  WHERE threads._id = new.thread_id  AND (new.reserved = 0 OR (new.reserved = 1 AND new.type = 3)); END;
CREATE TRIGGER sms_update_thread_safe_message_on_update AFTER  UPDATE OF body, date, safe_message  ON sms BEGIN  UPDATE threads SET    safe_message = new.safe_message  WHERE threads._id = new.thread_id; END;
CREATE INDEX typeThreadIdIndex ON sms (type, thread_id);
CREATE INDEX index_date_ordered_sms ON sms (thread_id, date DESC);"""
    f = d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"{query}\\\"\"")
    print(f)


def add_random_call(d, tel_phone=None, region='ru'):
    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=7)
    now = int(now.strftime("%s"))
    week_ago = int(week_ago.strftime("%s"))
    randtime = (week_ago + random.randint(0, now-week_ago)) * 1000
    if region == 'us':
        phone = '+' + str(random.randint(10000000000, 19999999999))
    elif region == 'in':
        phone = '+' + str(random.randint(628000000000, 628999999999))
    else:
        phone = '+' + str(random.randint(79000000000, 79999999999))

    # Звоним кому-то из контактов клиентов
    phone = tel_phone if tel_phone else phone

    if region == 'in':
        formatted_phone = phone[0:3] + ' ' + phone[3:6] + ' ' + phone[6:9] + '-' + phone[9:11] + '-' + phone[11:13]
    else:
        formatted_phone = phone[0:2] + ' ' + phone[2:5] + ' ' + phone[5:8] + '-' + phone[8:10] + '-' + phone[10:12]

    types = [1, 2, 3]
    type = random.choice(types)
    duration = random.randint(0, 120) if type in (1, 2) else 0
    features = 4 if type in (1, 2) else 0
    query = f"insert into calls(number, date, duration, type, features, subscription_component_name, subscription_id, new, countryiso, is_read, geocoded_location, normalized_number, formatted_number, last_modified, sim_id, logtype, frequent, contactid, e164_number, spam_report, reject_flag, simnum,  sec_end_type, sec_stir_shaken) values ('{phone}', {randtime}, {duration}, {type}, {features}, 'com.android.phone/com.android.services.telephony.TelephonyConnectionService', '8970199210850398225F', 1, 'RU', 0, 'Russia', '{phone}', '{formatted_phone}', {randtime}, 1, 100, 1, 0, '{phone}', 0, 0, 2, 210500, 0);"
    d.shell(f"su -c /data/local/sqlite3 /data/data/com.samsung.android.providers.contacts/databases/calllog.db \"\\\"{query}\\\"\"")

def add_random_sms(d):
    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=7)
    now = int(now.strftime("%s"))
    week_ago = int(week_ago.strftime("%s"))
    randtime = (week_ago + random.randint(0, now-week_ago)) * 1000
    phone = '+' + str(random.randint(79000000000, 79999999999))
    formatted_phone = phone[0:2] + ' ' + phone[2:5] + ' ' + phone[5:8] + '-' + phone[8:10] + '-' + phone[10:12]
    types = [1, 2]
    type = random.choice(types)

    query = f"select _id from canonical_addresses where address = '{phone}'"
    address_id = d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"{query}\\\"\"").output
    if address_id == '':
        query = f"insert into canonical_addresses(address) values ('{phone}');"
        d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"{query}\\\"\"")
        query = f"select _id from canonical_addresses where address = '{phone}'"
        address_id = d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"{query}\\\"\"").output
    address_id = int(address_id)

    query = f"select _id from threads where recipient_ids = '{address_id}'"
    thread_id = d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"{query}\\\"\"").output
    if thread_id == '':
        query = f"insert into threads(date, recipient_ids, display_recipient_ids, snippet_type) values ({randtime}, '{address_id}', '{address_id}', 1);"
        d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"{query}\\\"\"")
        query = f"select _id from threads where recipient_ids = '{address_id}'"
        thread_id = d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"{query}\\\"\"").output
    thread_id = int(thread_id)

    query = f"insert into sms(thread_id, address, date, date_sent, protocol, type, reply_path_present, body, service_center, sub_id, creator, sim_slot, sim_imsi, correlation_tag) values ({thread_id}, '{phone}', {randtime}, {randtime}, 0, {type}, 0, '{generate_message()}', '+79037011111', 1, 'com.samsung.android.messaging', 1, '250992243268704', 'd34ccd79bc4a83be');"
    d.shell(f"su -c /data/local/sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db \"\\\"{query}\\\"\"")
