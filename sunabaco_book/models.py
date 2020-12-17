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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('タイトル', max_length=64, null=False)
    genre = models.CharField('本のジャンル', max_length=21, choices=BOOK_GENRE, null=False)
    Author = models.CharField('本の著者', max_length=32, null=False)
    body = models.TextField('本の説明', max_length=512, null=True)
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

# --------------------------本のレンタル履歴-------------------------------------
class Reservation(models.Model):
    """予約管理"""
    book_image = models.ForeignKey(Bookimage, on_delete=models.CASCADE)
    lending_user_id = models.UUIDField(editable=False)
    return_date = models.DateField(verbose_name='返却日 日付', blank=True, null=False,)
    book_id = models.UUIDField(editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __int__(self):
         return self.return_date

# ---------------------------Review------------------------------------
SCORE_CHOICES = (
    (1, '★1'),
    (2, '★2'),
    (3, '★3'),
    (4, '★4'),
    (5, '★5'),
)
class Review(models.Model):
    """評価"""
    point = models.IntegerField('評価点', choices=SCORE_CHOICES)
    body = models.TextField('本の感想', max_length=512, null=True)
    target = models.ForeignKey(Bookimage, verbose_name='評価対象の本', on_delete=models.CASCADE)

    def __str__(self):
        # 'よくわかるPythonの本 - ★5' のように返す
        return '{} - {}'.format(self.target.title, self.get_point_display())
