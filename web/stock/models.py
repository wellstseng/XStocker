from djongo import models
from django.contrib.auth.models import User
import logging 
logger = logging.getLogger('django')

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

    def add_stock(self, _stock_id:str):
        record = Record(stock_id=_stock_id)
        self.stock_list.append(record)
        self.save()

    def remove_stock(self, stock_id:str):
        idx = self.get_stock(stock_id)
        if idx == -1:
            return False
        else:
            del self.stock_list[idx]
            self.save()
            return True

    def get_stock(self, stock_id:str):
        find = -1
        for i in range(0, len(self.stock_list)):
            if self.stock_list[i].stock_id == stock_id:
                find = i
                break
        return find

    def has_stock(self, stock_id:str):
        return self.get_stock(stock_id) != -1

    def __str__(self):
        return "user:{0}, list: {1}".format(self.user.username, ','.join(str(x) for x in self.stock_list))