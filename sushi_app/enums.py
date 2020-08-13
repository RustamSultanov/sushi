
ST_SOLVED, ST_IN_PROGRESS, ST_NOT_SOLVED = range(3)
STATUS_CHOICE = (
    (ST_SOLVED, "Решен"),
    (ST_IN_PROGRESS, "Обрабатывается"),
    (ST_NOT_SOLVED, "Не решен"),
)


#Типы сообытий регистрируемые для оповещений
(TASK_T, MESSEGE_T, NEWS_T, 
 FEEDBACK_T, SHOP_T, MATERIALS_T,
 IDEA_T) = ('task', 'messege', 'news', 
 'feedback', 'shop', 'materials',
 'idea',)

EVENT_TYPE_CHOICES = (
    (TASK_T, 'Задачи'),
    (MESSEGE_T, 'Сообщения'),
    (NEWS_T, 'Новости'),
    (FEEDBACK_T, 'Отзывы'),
    (SHOP_T, 'Создание магазина'),
    (IDEA_T, 'Идеи'),
    (MATERIALS_T, 'Материалы')
)

#Селекторы пользовательской подписки  - принимать оповещения на сайте/по почте
REALTIME_C, EMAIL_C = ('site', 'email')
SUBSCRIBE_TYPE_CHOICES = (
    (REALTIME_C, 'На сайте'),
    (EMAIL_C, 'По почте')
)
