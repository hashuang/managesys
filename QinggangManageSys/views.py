from django.shortcuts import render, render_to_response


def handler404(request):
    return render(request, '404.html', status=404)

def paralle_test1():
    with open('/Users/changxin/mission/qinggang/QinggangManageSys/QinggangManageSys/test_crontab.txt','a') as f:
        f.write("hello\n")
