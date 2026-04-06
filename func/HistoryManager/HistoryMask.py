

class HistoryMask():
    def __init__(self, blueprint):

        # Проходимся по всем схемам и добавляем их как DataScheme
        self.saved_schemes = []
        for scheme in blueprint.schemes:
            dataScheme = scheme.get_scheme_data_save()
            self.saved_schemes.append(dataScheme)

        # Так же с комментариями
        self.saved_comments = []
        for comment in blueprint.comments:
            dataComment = comment.get_comment_data()
            self.saved_comments.append(dataComment)