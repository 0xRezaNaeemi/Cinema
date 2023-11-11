from django.db import models


class Movie(models.Model):
    """
    Represents a movie
    """
    name = models.CharField(verbose_name='عنوان', max_length=100, null=True, blank=True)
    director = models.CharField(verbose_name='کارگردان', max_length=50, null=True, blank=True)
    year = models.IntegerField(verbose_name='سال تولید', null=True, blank=True)
    length = models.IntegerField(verbose_name='مدت زمان', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    poster = models.ImageField(verbose_name='پوستر', upload_to='movie_poster/', null=True)

    class Meta:
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم'

    def __str__(self):
        return self.name


class Cinema(models.Model):
    """
    Represents a cinema saloon
    """
    cinema_code = models.IntegerField(verbose_name='کد سینما', primary_key=True, unique=True)
    name = models.CharField(verbose_name='عنوان', max_length=50, null=True, blank=True)
    city = models.CharField(verbose_name='شهر', max_length=50, default='تهران')
    capacity = models.IntegerField(verbose_name='ظرفیت', null=True, blank=True)
    phone = models.CharField(verbose_name='شماره تماس', max_length=11, null=True, blank=True)
    address = models.TextField(verbose_name='آدرس', null=True, blank=True)
    image = models.ImageField(verbose_name='تصویر سینما', upload_to='cinema_image/', null=True)

    class Meta:
        verbose_name = 'سینما'
        verbose_name_plural = 'سینما'

    def __str__(self):
        return self.name


class Ticket(models.Model):
    pass


class ShowTime(models.Model):
    """
    Represents a movie in a cinema at a specific time
    """
    SALE_NOT_STARTED = 1
    SALE_OPEN = 2
    TICKETS_SOLD = 3
    SALE_CLOSED = 4
    MOVIE_PLAYED = 5
    SHOW_CANCELED = 6
    STATUS_CHOICES = (
        (SALE_NOT_STARTED, 'فروش آغاز نشده'),
        (SALE_OPEN, 'در حال فروش بلیت'),
        (TICKETS_SOLD, 'بلیت‌ها تمام شد'),
        (SALE_CLOSED, 'فروش بلیت بسته شد'),
        (MOVIE_PLAYED, 'فیلم پخش شد'),
        (SHOW_CANCELED, 'سانس لغو شد'),
    )
    movie = models.ForeignKey('Movie', verbose_name='فیلم', on_delete=models.PROTECT)
    cinema = models.ForeignKey('Cinema', verbose_name='سینما', on_delete=models.PROTECT)
    start_time = models.DateTimeField(verbose_name='زمان شروع نمایش', )
    price = models.IntegerField(verbose_name='قیمت', )
    salable_seats = models.IntegerField(verbose_name='صندلی های قابل فروش', )
    free_seats = models.IntegerField(verbose_name='صندی های خالی', )
    status = models.IntegerField(verbose_name='وضیعت', choices=STATUS_CHOICES, default='SALE_NOT_STARTED')

    class Meta:
        verbose_name = 'سکانس'
        verbose_name_plural = 'سکانس'

    def __str__(self):
        return '{} - {} - {}'.format(self.movie, self.cinema, self.start_time)

    def get_price_display(self):
        return '{} تومان'.format(self.price)

    def is_full(self):
        """
        Returns True if all seats are sold
        """
        return self.free_seats == 0

    def open_sale(self):
        """
        Opens ticket sale
        If sale was opened before, raises an exception
        """
        if self.status == ShowTime.SALE_NOT_STARTED:
            self.status = ShowTime.SALE_OPEN
            self.save()
        else:
            raise Exception('Sale has been started before')

    def close_sale(self):
        """
        Closes ticket sale
        If sale is not open, raises an exception
        """
        if self.status == ShowTime.SALE_OPEN:
            self.status = ShowTime.SALE_CLOSED
            self.save()
        else:
            raise Exception('Sale is not open')

    def expire_showtime(self, is_canceled=False):
        """
        Expires showtime and updates the status
        :param is_canceled: A boolean indicating whether the show is canceled or not, default is False
        """
        if self.status not in (ShowTime.MOVIE_PLAYED, ShowTime.SHOW_CANCELED):
            self.status = ShowTime.SHOW_CANCELED if is_canceled else ShowTime.MOVIE_PLAYED
            self.save()
        else:
            raise Exception('Show has been expired before')
