from django.views import View
from django.shortcuts import render

from bbs.models import Topics, Categories


class CategoryView(View):
    default_order = "-create_time"

    order_list = ["-create_time", "-view_count"]

    categories = [1, 2, 3, 4]

    def get(self, request, category_id):
        order = request.GET.get("order", "-create_time")
        # 防止用户擅自篡改order的值
        if order not in self.order_list:
            order = self.default_order
        if category_id not in self.categories:
            category_id = 1
        topics = Topics.objects.filter(category_id=category_id).order_by(order).all()
        category = Categories.objects.filter(id=category_id).first()

        return render(request, "root/index.html", {"topics": topics, "category": category, "order": order})
