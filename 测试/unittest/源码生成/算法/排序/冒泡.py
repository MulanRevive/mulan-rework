# 参考: https://stackabuse.com/sorting-algorithms-in-python/
def 冒泡(数列):
  换过 = True
  while 换过:
    换过 = False
    for i in range(0, len(数列) - 1):
      前项 = 数列[i]
      后项 = 数列[i + 1]
      if 前项 > 后项:
        数列[i], 数列[i + 1] = 后项, 前项
        换过 = True

打乱数列 = [5, 2, 1, 8, 4]
冒泡(打乱数列)
print(打乱数列)