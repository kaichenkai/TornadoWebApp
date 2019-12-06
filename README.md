# TornadoWebApp
基于 tornado 框架 + bootstrap 构建的 web 应用
 - 将mysql里边存储的统计信息进行展示
 - 能够对统计信息分页展示, 查询操作

原文地址: https://www.cnblogs.com/kaichenkai/p/11999880.html

<br>


## 部署服务：

##### 接入违法数据，则按以下步骤进行:

1. `python3` 的环境
2. 在 `settings/setting.py` 文件中, 确认 `mysql` 对应的信息（用户名，密码，IP地址，端口）是否正确

<br>

## 运行服务：

##### 在 `TornadoWeb` 目录下进行

##### 开启服务：
   ```shell
   启动程序监听 9000（默认）端口：
   sh run.sh start
   ```

##### 关闭服务：
   ```shell
   关闭监听 9000（默认）端口：
   sh run.sh stop
   ```

##### 查看服务监听状态：
   ```shell
   查看 9000 端口（默认）监听状态：
   sh run.sh status
   ```

<br>

## url 路由：

##### 查询url：
   ```shell
   http://ip:9000/illegal/stats
   ```

<br>


##### 完

<br>
