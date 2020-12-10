from PIL import Image
from io import BytesIO
from django.core.files import File
from django.db import models
from django.utils import timezone
import os
import uuid

def upload_to_portfolio(self, filename):
    ext = filename.split('.')[-1]  #filename->sample.png->splitすると['sample', 'png']
    name = '{}.{}'.format(uuid.uuid4(), ext)
    return os.path.join('portfolio', name)

# -------------------------------------------------------------------

class Portfolio(models.Model):
    title = models.CharField('タイトル', max_length=64, null=False)
    body = models.TextField('内容', max_length=512, null=False)
    image = models.ImageField('画像', upload_to='upload_to_portfolio', null=False)
    pickup = models.IntegerField(default=0, null=False)

    def save(self, new_image=False, *args, **kwargs):
        # インスタンスメソッドの上書き
        # 画像があれば圧縮して新しい画像オブジェクトを作成する
        if new_image:
            new_image = Portfolio.compress(self.image)
            self.image = new_image
        super().save(*args, **kwargs)

    @classmethod
    def compress(cls, image):
        # RGBA 対応した処理
        # 画像の読み込み
        im = Image.open(image)
        # バイナリデータを扱う
        im_io = BytesIO()
        # RGBA判定
        if im.mode == 'RGBA':
            im.load()
            # RGBで背景真っ白、サイズはdefault
            background = Image.new('RGB', im.size, (255, 255, 255))
            # 背景真っ白に画像を貼り付ける
            background.paste(im, mask=im.split()[3])
            # 圧縮して保存
            background.save(im_io, 'JPEG', Quality=70)
        else:
            im = im.convert('RGB')
            im.save(im_io, 'JPEG', quality=70)

        # djangoで保存できるようにfileオブジェクトにする
        new_image = File(im_io, name=image.name)
        return new_image

# ---------------------------profile------------------------------------
class profile(models.Model):
    name = models.CharField('名前', max_length=64, null=False)
    body = models.TextField('自己紹介', max_length=512, null=False)
    image = models.ImageField('画像', upload_to='upload_to_profile', null=False)

    def save(self, new_image=False, *args, **kwargs):
        # インスタンスメソッドの上書き
        # 画像があれば圧縮して新しい画像オブジェクトを作成する
        if new_image:
            new_image = Portfolio.compress(self.image)
            self.image = new_image
        super().save(*args, **kwargs)

    @classmethod
    def compress(cls, image):
        # RGBA 対応していない処理
        im = Image.open(image)
        im_io = BytesIO()
        im.save(im_io, 'JPEG', quality=70)
        new_image = File(im_io, name=image.name)
        return new_image

# ---------------------------comment------------------------------------
JOB_CHOICES = [
    ('デザイン', 'デザイン'),
    ('ホームページ制作', 'ホームページ制作'),
    ('コーポレートサイト', 'コーポレートサイト'),
    ('LP制作', 'LP制作'),
    ('レスポンシブデザイン、webサイト修正依頼', 'レスポンシブデザイン、webサイト修正依頼'),
    ('その他', 'その他'),
]
class Comment(models.Model):
    name = models.CharField('お名前', max_length=64, null=False)
    client_email = models.EmailField('Email', max_length=255, null=False)
    job = models.CharField('お問い合わせ（カテゴリ）', max_length=21, choices=JOB_CHOICES, null=False)
    text = models.TextField('依頼内容', max_length=512, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

