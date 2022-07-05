from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from accounts.models import User


class Politic(models.Model):
    politic_slug = models.SlugField(max_length=50, db_index=True, unique=True, allow_unicode=True)
    poli_nm = models.CharField(max_length=20, null=False, unique=True) # 정치인 이름
    poli_ch_nm = models.CharField(max_length=30, null=False) # 정치인 이름 한문
    img_link = models.CharField(max_length=50, null=False, unique=True) # 이미지 링크
    birth = models.CharField(max_length=15, null=False) # 생년월일
    career = models.TextField(max_length=1500, null=False) # 경력
    party_af = models.CharField(max_length=50, null=False) # 소속정당이름

    def __str__(self):
        return self.poli_nm

    class Meta:
        db_table = 'politic'
        verbose_name = '정치인 정보'
        index_together = [['id', 'politic_slug']]

    def get_absolute_url(self):
        return reverse('politic:politic_detail', args=[self.id, self.politic_slug])  # 상세페이지, 모델 출력시 이부분을 출력하고 주소가 자동으로 됨


class Rating(models.Model):
    rate_num = models.AutoField(primary_key=True)
    user_nk = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rating')
    politic = models.ForeignKey(Politic, on_delete=models.CASCADE, related_name='politic_number')
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.CharField(max_length=100)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField(User, related_name='likse', blank=True)
    dislike = models.ManyToManyField(User, related_name='dislikes', blank=True)

    class Meta:
        db_table = 'rating'
