## 请求地址

```
POST /api/funds/withdrawal/
```

## 请求头

参数 | 说明 | 取值范围 | 示例 |
--- | --- | --- | ---
platform | 平台 | wechat | wechat
usertype | 用户类型 | doctor | doctor
Authorization | 认证头 | basic与后面的值 中间以空格隔开 | basic {uid}

`Authorization`说明

- 测试环境  basic {uid} // 代表登录对象的uid, 如usertype是doctor就填doctor的uid

- 正式环境 bearer {token} // 代表授权令牌，需要授权的接口都要加上

## 请求数据

- 参数说明

参数 | 说明 | 取值范围 | 示例 |
--- | --- | --- | ---
fullname | 持卡人姓名 | str | 持卡人姓名
amount | 提现金额 | float | 10
cardno | 银行卡号 | str | 64634256435
account_bank | 开户行 | str | 开户行
sms_code | 提现验证码 | str | 123456

```json
{
    "fullname": "持卡人姓名",
    "amount": 10,
    "cardno": "64634256435",
    "account_bank": "开户行",
    "sms_code": "123456"
}
```

## 返回数据


- 请求成功
```json
{
    "errmsg": "提交成功!"
}
```

- 请求失败
```json
{
    "errmsg": "您的可提现金额不足!"
}
```
