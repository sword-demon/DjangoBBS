from django.core.paginator import Paginator, EmptyPage
from django.views import View
from django.shortcuts import render

from bbs.models import Topics, Categories


# from utils.page import Pagination


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
        current_page = int(request.GET.get("page", 1))

        paginator = Paginator(topics, 20)

        if paginator.num_pages > 11:
            if current_page - 5 < 1:
                page_range = range(1, 11)
            elif current_page + 5 > paginator.num_pages:
                page_range = range(paginator.num_pages - 11, paginator.num_pages + 1)
            else:
                page_range = range(current_page - 5, current_page + 5)
        else:
            page_range = paginator.page_range

        try:
            current = paginator.page(current_page)
        except EmptyPage as e:
            current = paginator.page(1)

        return render(request, "root/index.html",
                      {"topics": current, "category": category, "order": order, "page_range": page_range,
                       "length": len(topics)})
