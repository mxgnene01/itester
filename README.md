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

## 原理

- 使用 `nose` 自带的html插件及功能来发现case，执行case
- 使用 `parameterized` 进行case 的参数化