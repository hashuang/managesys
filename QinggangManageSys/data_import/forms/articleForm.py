#coding:utf-8
from django import forms
from DjangoUeditor.forms import UEditorField, UEditorModelForm
from ccx_blog.models import Article,Reply

class ReplyForm(forms.Form):
    nickname = forms.CharField(error_messages={
        'required':u'请填写你的名称'
    })
    content = UEditorField("描述",initial="abc",width=600,height=800)

    # class Meta:
    #     model=Reply
    #     fields = ['nickname','content']