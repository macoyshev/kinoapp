from flask_admin.contrib.sqla import ModelView

from app.db.models import Review


class UserView(ModelView):
    can_edit = True
    can_create = False
    can_delete = False
    can_view_details = True

    column_list = ['name', 'reviews']

    form_excluded_columns = ['password', 'salt', 'name']
    form_columns = ('reviews',)
    inline_models = (
        (
            Review,
            {
                'form_columns': ('id', 'comment'),
            },
        ),
    )


class MovieModel(ModelView):
    can_create = True
    can_edit = True

    form_columns = ('title',)


class ReviewModel(ModelView):
    can_delete = False
    can_create = False
    can_edit = True

    column_list = ['comment', 'rating', 'user_id', 'movie_id']

    form_columns = ['comment']
