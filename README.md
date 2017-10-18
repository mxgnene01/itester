# itester

## 要求

- nose
- requests

## 介绍

看了不少测试环境 py.test、nose、unittest 对于QA 来说，书写case 需要写代码，所以简单写了一个使用Excel 维护case 的工具

## 使用命令

```
nosetests -s -v test_main.py --with-html --html-report=result/a.html
```