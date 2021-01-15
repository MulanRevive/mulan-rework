from enum import Enum, unique

@unique
class 语法(Enum):
    # 语法名称, 英文为原代码中对应名称. 按定义的先后顺序
    模块 = 'start'
    块 = 'block'
    注水声明列表 = 'stmt_list'
    声明列表 = 'stmt_list_'
    声明 = 'stmt'
    类型定义 = 'type_define'
    各基准类 = 'bases'
    类型主体 = 'type_body'
    各类型内声明 = 'type_stmts'
    类型内声明 = 'type_stmt'
    应变属性 = 'property'
    操作符 = 'operator'
    操作数 = 'op_arg'
    二元操作符 = 'bin_op'
    模块位置 = 'module_name_'
    引用声明 = 'using_stmt'
    各模块名 = 'module_name'
    模块名 = 'module_names'
    表达式声明 = 'expr_stmt'
    表达式前缀 = 'prefix_expr'
    赋值 = 'assignment'
    外部声明 = 'declaration'
    增量赋值 = 'aug(ment)_assign'
    返回声明 = 'return_stmt'
    终止声明 = 'break_stmt'
    跳过声明 = 'continue_stmt'
    试试声明 = 'try_stmt'
    抛出声明 = 'throw_stmt'
    顺便处理 = 'withitem'
    各接手声明 = 'catch_stmts'
    接手声明 = 'catch_stmt'
    表达式 = 'expr'
    各表达式前缀 = 'prefix_exprs'
    片 = 'slice'
    数 = 'number'
    字符串 = 'string'
    列表表达式 = 'list_expr'
    多项式乘法 = 'factor_expr'
    字典表达式 = 'dict_expr'
    各键值对 = 'kv_pairs'
    键值对 = 'kv_pair'
    常量 = 'name_const'
    二元表达式 = 'bin_expr'
    一元表达式 = 'unary_expr'
    三元表达式 = 'ternary_expr'
    首要表达式 = 'primary_expr'
    范围表达式 = 'range_expr'
    调用 = 'call'
    超类 = 'super'
    lambda形参 = 'lambda_param',
    lambda主体 = 'lambda_body',
    lambda表达式 = 'lambda_expr',
    匿名函数 = 'lambda_func'
    类型名称 = 'type_name'
    实参部分 = 'arguments'
    各名称 = 'names'
    各实参 = 'args'
    各表达式 = 'exprs'
    变量 = 'var'
    实参 = 'arg'
    形参列表 = 'param_list'
    非空形参列表 = 'param_list_not_empty'
    形参 = 'param'
    函数 = 'function'
    条件声明 = 'if_stmt'
    否则如果声明 = 'elif_stmt'
    每当声明 = 'while_stmt'
    迭代器 = 'iterator'
    遍历范围 = 'loop_range'
    对于声明 = 'for_stmt'
    名称 = 'name'

    def 成分(self, *成分):
        文本 = []
        for 各成分 in 成分:
            if isinstance(各成分, Enum):
                文本.append(各成分.name)
            else:
                文本.append(各成分)
        return self.name + " : " + " ".join(文本)
