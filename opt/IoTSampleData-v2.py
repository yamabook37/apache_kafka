import random
import json
import time
from datetime import date, datetime
from collections import OrderedDict
import argparse
import string
import pprint
from faker.factory import Factory
from kafka import KafkaProducer
from kafka import KafkaConsumer

# ダミーデータ作成のための Faker の使用
Faker = Factory.create
fake = Faker()
fake = Faker("ja_JP")

# IoT機器のダミーセクション(小文字アルファベットを定義)
section = string.ascii_uppercase


# IoT機器で送信JSONデータの作成
def iot_json_data(count, proc):
    iot_items = json.dumps({
        'items': [{
            'id': i,                            # id
            'time': generate_time(),            # データ生成時間
            'proc': proc,                       # データ生成プロセス　 ：プログラム実行時のパラメータ
            'section': random.choice(section),  # IoT機器セクション　　：A-Z文字をランダムに割当
            'iot_num': fake.zipcode(),          # IoT機器番号　　　　：郵便番号をランダムに割当
            'iot_state': fake.prefecture(),     # IoT設置場所　　　　：都道府県名をランダムに割当
            'vol_1': random.uniform(100, 200),  # IoT値−１　　　　　  ：100-200の間の値をランダムに割当（小数点以下、14桁）
            'vol_2': random.uniform(50, 90)     # IoT値−２　　　　　　：50-90の間の値をランダムに割当（小数点以下、14桁）
            } 
            for i in range(count)
        ]
    }, ensure_ascii=False).encode('utf-8')
    return iot_items


# IoT機器で計測されたダミーデータの生成時間
def generate_time():
    dt_time = datetime.now()
    gtime = json_trans_date(dt_time)
    return gtime

# date, datetimeの変換関数
def json_trans_date(obj):
    # 日付型を文字列に変換
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    # 上記以外は対象外.
    raise TypeError ("Type %s not serializable" % type(obj))


# メイン : ターミナル出力用
def tm_main(count, proc):
    print('ターミナル 出力')
    iotjsondata = iot_json_data(count, proc)
    json_dict = json.loads(iotjsondata)
    pprint.pprint(json_dict)


# メイン : Kafka出力用
def kf_main(count, proc):
    print('Kafka 出力')
    iotjsondata = iot_json_data(count, proc)
    json_dict = json.loads(iotjsondata)

    producer = KafkaProducer(bootstrap_servers=['broker:29092'])
    date = datetime.now().strftime("%Y/%m/%d")

    for item in json_dict['items']:
        # print(item)
        # result = producer.send('topic-01', json.dumps(item).encode('utf-8'))
        result = producer.send('topic-01', key=date.encode('utf-8'), value=json.dumps(item).encode('utf-8'))

    print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IoT機器のなんちゃってダミーデータの生成')
    parser.add_argument('--count', type=int, default=10, help='データ作成件数')
    parser.add_argument('--proc', type=str, default='111', help='データ作成プロセス名')
    parser.add_argument('--mode', type=str, default='tm', help='tm（ターミナル出力）/ kf（Kafka出力）')
    args = parser.parse_args()

    start = time.time()

    if (args.mode == 'kf'): 
        kf_main(args.count, args.proc)
    else :
        tm_main(args.count, args.proc)

    making_time = time.time() - start

    print("")
    print(f"データ作成件数:{args.count}")
    print("データ作成時間:{0}".format(making_time) + " [sec]")
    print("")
