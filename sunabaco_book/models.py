from PIL import Image
from io import BytesIO
from django.core.files import File
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator 
import os
import uuid

def upload_to_book(self, filename):
    ext = filename.split('.')[-1]  #filename->sample.png->splitすると['sample', 'png']
    name = '{}.{}'.format(uuid.uuid4(), ext)
    return os.path.join('sunabaco_book', name)

# -------------------------------------------------------------------
BOOK_GENRE = [
    ('デザイン', 'デザイン'),
    ('ビジネス', 'ビジネス'),
    ('プログラミング', 'プログラミング'),
    ('社会', '社会'),
    ('その他', 'その他'),
]

class Bookimage(models.Model):
    title = models.CharField('タイトル', max_length=64, null=False)
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.CharField('本のジャンル', max_length=21, choices=BOOK_GENRE, null=False)
    Author = models.CharField('本の著者', max_length=32, null=False)
    body = models.TextField('本の説明', max_length=512, null=False)
    image = models.ImageField('本のイメージ', upload_to='upload_to_book', null=False)
    lending = models.PositiveSmallIntegerField('レンタルモード', default=0, validators=[MinValueValidator(0), MaxValueValidator(3)], null=False)
    book_status = models.PositiveSmallIntegerField('本の貸し出し状態', default=0, validators=[MinValueValidator(0), MaxValueValidator(2)], null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, new_image=False, *args, **kwargs):
        # インスタンスメソッドの上書き
        # 画像があれば圧縮して新しい画像オブジェクトを作成する
        if new_image:
            new_image = Bookimage.compress(self.image)
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

# ---------------------------------------------------------------
class Reservation(models.Model):
    """予約管理"""
    user_id = models.PositiveIntegerField(editable=False)
    return_date = models.DateField(verbose_name='サンプル項目1 日付', blank=True, null=True,)
    isbn = models.CharField('ISBN', max_length=13)
    
# # ---------------------------comment------------------------------------
# JOB_CHOICES = [
#     ('デザイン', 'デザイン'),
#     ('ホームページ制作', 'ホームページ制作'),
#     ('コーポレートサイト', 'コーポレートサイト'),
#     ('LP制作', 'LP制作'),
#     ('レスポンシブデザイン、webサイト修正依頼', 'レスポンシブデザイン、webサイト修正依頼'),
#     ('その他', 'その他'),
# ]
# class Comment(models.Model):
#     name = models.CharField('お名前', max_length=64, null=False)
#     client_email = models.EmailField('Email', max_length=255, null=False)
#     job = models.CharField('お問い合わせ（カテゴリ）', max_length=21, choices=JOB_CHOICES, null=False)
#     text = models.TextField('依頼内容', max_length=512, null=False)
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.text

