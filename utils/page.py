class ShowPage(object):
    def __init__(self, page_num, total_count, url_prefix, per_page=10, max_page=11):
        '''
        :param page_num: 当前页码数
        :param total_count: 数据总数
        :param url_prefix: a 标签 href 的前缀
        :param per_page: 每页展示的数据数
        :param max_page: 页面上最多显示的页码数
        '''
        self.url_prefix = url_prefix
        self.max_page = max_page

        # 总共需要多少页码来显示
        total_page, m = divmod(total_count, per_page)

        # 如果还有数据
        if m:
            total_page += 1
        self.total_page = total_page

        try:
            page_num = int(page_num)
            # 如果输入的页码数超过了最大的页码数，默认返回最后一页
            if page_num > self.total_page:
                page_num = self.total_page
            # 如果输入的页码数小于 1，则返回第一页
            if page_num < 1:
                page_num = 1
        except Exception as e:
            # 当输入的页码不是正经数字的时候 默认返回第一页的数据
            page_num = 1
        self.page_num = page_num

        # 定义两个变量保存数据从哪儿取到哪儿
        self.data_start = (self.page_num - 1) * 10
        self.data_end = self.page_num * 10

        # 页面上总共展示多少页码
        if self.total_page < self.max_page:
            self.max_page = self.total_page

        half_max_page = self.max_page // 2

        # 页面上展示的页码的开始页
        page_start = self.page_num - half_max_page
        # 页面上展示的页码的结束页
        page_end = self.page_num + half_max_page
        # 如果当前页减一半比 1 还小
        if page_start <= 1:
            page_start = 1
            page_end = self.max_page
        # 如果当前页加一半比总页码还大
        if page_end >= self.total_page:
            page_end = self.total_page
            page_start = self.total_page - self.max_page + 1
        self.page_start = page_start
        self.page_end = page_end

    @property
    def start(self):
        return self.data_start

    @property
    def end(self):
        return self.data_end

    def page_html(self):
        # 拼接 html 的分页代码
        html_list = []

        # 添加首页按钮
        html_list.append('<li><a href="{}?page=1">首页</a></li>'.format(self.url_prefix))

        # 如果是第一页，就没有上一页
        if self.page_num <= 1:
            html_list.append(
                '<li class="disabled"><a href="#"><span aria-hidden="true">«</span></a></li>'.format(self.page_num - 1))
        else:
            # 加一个上一页的标签
            html_list.append(
                '<li><a href="{}?page={}"><span aria-hidden="true">«</span></a></li>'.format(self.url_prefix,
                                                                                             self.page_num - 1))

        # 展示的页码
        for i in range(self.page_start, self.page_end + 1):
            # 给当前页添加 active
            if i == self.page_num:
                tmp = '<li class="active"><a href="{0}?page={1}">{1}</a></li>'.format(self.url_prefix, i)
            else:
                tmp = '<li><a href="{0}?page={1}">{1}</a></li>'.format(self.url_prefix, i)
            html_list.append(tmp)

        # 如果是最后一页，就没有下一页
        if self.page_num >= self.total_page:
            html_list.append('<li class="disabled"><a href="#"><span aria-hidden="true">»</span></a></li>')
        else:
            html_list.append(
                '<li><a href="{}?page={}"><span aria-hidden="true">»</span></a></li>'.format(self.url_prefix,
                                                                                             self.page_num + 1))

        # 添加尾页按钮
        html_list.append('<li><a href="{}?page={}">尾页</a></li>'.format(self.url_prefix, self.total_page))

        page_html = "".join(html_list)  # 拼接 html 的分页代码
        return page_html
