from djongo import models
from django.contrib.auth.models import User

class Record(models.Model):
    stock_id = models.CharField(max_length=20)

    class Meta:
        abstract = True

    def __str__(self):
        return self.stock_id


class Overview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_list = models.ArrayModelField(
        model_container=Record,
    )

    def add(self, _stock_id:str):
        record = Record(stock_id=_stock_id)
        self.stock_list.append(record)
        self.save()

    def has_stock(self, stock_id:str):
        find = False
        for d in self.stock_list:
            if d.stock_id == stock_id:
                find = True
                break

    def __str__(self):
        return "user:{0}, list: {1}".format(self.user.username, ','.join(str(x) for x in self.stock_list))