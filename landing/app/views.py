from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    param = request.GET.get('from-landing')
    if param:
        counter_click.update({param})
        print(param)
    print(sum(counter_click.values()))
    return render_to_response('index.html')


def landing(request):
    param = request.GET.get('ab-test-arg')
    counter_show.update({param})
    if param == 'test':
        return render_to_response('landing_alternate.html')
    elif param == 'original':
        return render_to_response('landing.html')
    else:
        return render_to_response('index.html')


def stats(request):
    try:
        marker_test = counter_click['test'] / counter_show['test']
    except:
        marker_test = 0.0
    try:
        marker_original = counter_click['original'] / counter_show['original']
    except:
        marker_original = 0.0
    return render_to_response('stats.html', context={
            'test_conversion': marker_test,
            'original_conversion': marker_original,
        })
