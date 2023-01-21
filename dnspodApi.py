# -*- encoding:utf-8 -*-
import time
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models


def change_dns(SecretId, SecretKey, Domain, SuDomain, RecordType, RecordId: int, Value, TTL=None):
    r"""修改dns记录

    :param SecretId:
    :param SecretKey:
    :param Domain: 域名
    :param SuDomain: 主机记录
    :param RecordType: 记录类型
    :param RecordId: 记录Id
    :param Value: 记录值
    :param TTL: TTL值
    :return: 操作结果
    """
    for i in range(5):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(SecretId, SecretKey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "dnspod.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = dnspod_client.DnspodClient(cred, "", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.ModifyRecordRequest()
            params = {
                "Domain": Domain,  # 域名
                "DomainId": None,  # 域名id，优先级高于域名
                "SubDomain": SuDomain,  # 主机记录
                "RecordType": RecordType,  # 记录类型
                "RecordLine": "默认",  # 记录线路
                "RecordLineId": None,  # 记录线路id，优先级高于记录线路
                "Value": Value,  # 记录值，IP
                "MX": None,  # MX优先级
                "TTL": TTL,  # TTL 0-604800
                "Status": None,  # 记录状态
                "RecordId": RecordId  # 记录id
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个ModifyRecordResponse的实例，与请求对象对应
            resp = client.ModifyRecord(req)
            # 输出json格式的字符串回包
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]" + resp.to_json_string())
            return True

        except TencentCloudSDKException as err:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]第{i + 1}次请求失败\n错误：{err}")

    return False


if __name__ == "__main__":
    change_dns("AKIDwiFVUCdngaDZeSzFEwMVNyIM9fusa1B4", "dz4sPecJjslOkpc9QQ9akcEZeSzFEgrl", "yigefz.net", "server",
               "AAAA", 1316792446, "240e:335:4881:6b90:731:cce3:233f:ef62")
