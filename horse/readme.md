一个目录就是一种木马，所有木马都必须生成HeaderHorse得以利用（header类型）

`UndeadHeaderHorse`  不死马
`WormHeaderHorse`  蠕虫马(在所有php文件头部加上马)

木马目录结构：
```
├─UndeadHeaderHorse
│  │  Horse.php   # 木马代码，激活后生成HeaderHorse
│  │  Horse.py    # 激活木马
```

上传的原始木马名字都叫`Horse.php`
