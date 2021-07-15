from utils.decorator import check_login


class LoginRequiredMixin(object):
    @staticmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return check_login(view)
