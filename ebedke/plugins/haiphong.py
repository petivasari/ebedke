from datetime import datetime, timedelta
from ebedke.utils.date import days_lower, on_workdays
from ebedke.utils import facebook
from ebedke.pluginmanager import EbedkePlugin

FB_PAGE = "https://www.facebook.com/Haiphongvietnamesekitchen/"
FB_ID = "271018510265811"

@on_workdays
def getMenu(today):
    is_today = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() == today.date()
    menu_keywords = ["mai menü", "napi menü", "napi ebéd", "ebédmenü", "ebéd menü", days_lower[today.weekday()]]
    menu_filter = lambda post: is_today(post['created_time']) and any(word in post['message'].lower() for word in menu_keywords)
    menu = facebook.get_filtered_post(FB_ID, menu_filter)
    drop_words = ["11:", "36303366888", "1590", "mindenkit", "napi ebéd", "minden menü",
                  "étlapunk", "csodás", "foglalj", "házi limonádé", "üveges üdítő", "sörök", days_lower[today.weekday()]]
    menu = (line.strip("-+ ") for line in menu.splitlines() if not any(word in line.lower() for word in drop_words))

    return menu

plugin = EbedkePlugin(
    enabled=True,
    groups=["corvin"],
    name='Hai Phong Restaurant',
    id='sst',
    url=FB_PAGE,
    downloader=getMenu,
    ttl=timedelta(hours=23),
    cards=[],
    coord=(47.484781, 19.073096)
)
