from wagtail.models import Page

'''root_page = Page.objects.get(url_path='/')
level_one_pages = root_page.get_children().live().in_menu()
print(level_one_pages)
for level_one_page in level_one_pages:
    level_two_pages = level_one_page.get_children().live().in_menu()
    for level_two_page in level_two_pages:
        level_three_pages = level_two_page.get_children().live().in_menu()
        for level_three_page in level_three_pages:
            print(level_three_page.url_path)'''
        
def menu_pages(request):
    root_page = Page.objects.get(url_path='/')
    level_one_pages = root_page.get_children().live().in_menu()

    menu = []
    for level_one_page in level_one_pages:
        level_two_pages = level_one_page.get_children().live().in_menu()
        for level_two_page in level_two_pages:
            level_three_pages = level_two_page.get_children().live().in_menu()
            menu_item = {
                'level_two_page': level_two_page,
                'level_three_pages': level_three_pages,
            }
            menu.append(menu_item)

    return {'menu': menu}

