# 🖼️ My Images - GitHub 图床

图片托管仓库，用于各平台的图片上传。

## 📁 目录结构

| 目录 | 用途 |
|------|------|
| xiaohongshu/ | 小红书图片 |
| wechat/ | 微信公众号图片 |
| weibo/ | 微博图片 |
| blog/ | 博客图片 |
| other/ | 其他图片 |

## 🔗 图片 URL 格式

上传后，图片 URL 格式为：
https://raw.githubusercontent.com/twygreat/my-images/main/{目录}/{图片名}

例如：
https://raw.githubusercontent.com/twygreat/my-images/main/xiaohongshu/photo.jpg

## 📝 使用说明

使用 upload_image.py 脚本上传图片：
python upload_image.py <图片路径> <分类>

例如：
python upload_image.py photo.jpg xiaohongshu
