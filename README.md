# AWD的攻击框架

| Python版本 | 适用语言 | 版本   | 最近更新时间 |
| ---------- | -------- | ------ | ------------ |
| 3.x        | php      | V2.1.1 | 2020.8.10    |


## 改动
**v2.0.1**
增添了一些使用说明

**v2.0.2**

- 对 `undeath_horse.php` 删除了注释
- 修复了上传木马部分的bug（`lib.py`）
- 对所有的http请求都加上了burpsuite的代理：`127.0.0.1:8080`（`lib.py`）
- 修复了添加ip时的部分bug（`lib.py`）

**v2.0.3**

- 2020.7.28
- 对各处文本添加颜色，增加视觉冲击感亲切感
- 增加显示的函数 `Log.red() Log.green() Log.blue()`
- 命令提示符 `$` 显示在最左边，无空格，有颜色
- 增加config.py ，配置写在config对象内


**v2.1.0**
- 2020.8.9
- 结构重构、代码重构
- 可删除指定webshell
- 可自定义木马上传
- 可批量提交flag（需要完善flag提交代码）
- 可使用自定义exp批量攻击（需完善exp代码）
- 配置文件更改为config.json，可实时更新

**v2.1.1**

- 2020.8.10
- 完善代码
- 新增自定义发起请求（支持GET和POST请求）


## 使用

使用前配置config.json、开启burpsuite（端口号可以在config.json中改）

可以批量提交flag，需要自行完善提交flag的代码（位于`plugs/submit.py`）

可以自定义exp，需要自行完善exp代码（位于`plugs/exp1.py`）


安装第三方库

```
pip install -r requirements.txt
```

运行

```
python main.py
```

