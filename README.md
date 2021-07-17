# Django 开发 BBS + Blog

## 构建项目
```bash
django-admin startproject djangoBBS
```

## 导出当前项目需要的类库
```bash
# 安装
pip install pipreqs  # 或者 pip3 install pipreqs

# 使用
pipreqs .  # . 表示当前目录

# 使用建议，导出前先定位到当前项目根目录
pipreqs ./ --encoding=utf8 # 该命令避免编码错误
```

