#coding=utf-8
OK      = {'code': 0, 'message': '没有错误发生','success':0}
UNKNOWN = {'code': 100000, 'message': '未知错误','success':0}


class COMMON:
    NOTFOUND = {'code': 100001, 'message': 'API不存在.','success':0}
    INVALID_PARAM = {'code': 100002, 'message': '参数错误','success':0}
    PARAM_CONF_WRONG = {'code': 100003, 'message': '参数配置错误','success':0}

class USER:
    NOT_LOGIN = {'code': 200001, 'message': '请登录后继续浏览','success':0}
    REGISTER_FAILED = {'code': 200002, 'message': '添加用户失败','success':0}
    USER_EXIST = {'code': 200003, 'message': '用户已经存在','success':0}
    WRONG_PASSWORD_OR_USERNAME = {'code': 200004, 'message': '用户名或密码出错，请重试','success':0}
    NO_AUTHORITY = {'code': 200005, 'message': '您没有权限访问','success':0}
    CANNOT_DELETE_ADMIN = {'code': 200006, 'message': 'admin账号不能删除','success':0}
    USER_NOT_EXIST = {'code': 200007, 'message': '用户不存在','success':0}
