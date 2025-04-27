# 高德地图 MCP Server （Python版本）

这是高德地图 MCP Sever [https://github.com/zxypro1/amap-maps-mcp-server](https://github.com/zxypro1/amap-maps-mcp-server) 的Python克隆。

# 高德地图 MCP 服务工具列表

本服务提供以下工具：

## 1. maps_regeocode
将一个高德经纬度坐标转换为行政区划地址信息

**参数：**
- `location`: 经纬度坐标

## 2. maps_geo
将详细的结构化地址转换为经纬度坐标。支持对地标性名胜景区、建筑物名称解析为经纬度坐标

**参数：**
- `address`: 结构化地址
- `city` (可选): 指定查询的城市

## 3. maps_ip_location
IP 定位根据用户输入的 IP 地址，定位 IP 的所在位置

**参数：**
- `ip`: IP地址

## 4. maps_weather
根据城市名称或者标准adcode查询指定城市的天气

**参数：**
- `city`: 城市名称或者adcode

## 5. maps_bicycling
骑行路径规划用于规划骑行通勤方案，规划时会考虑天桥、单行线、封路等情况。最大支持 500km 的骑行路线规划

**参数：**
- `origin`: 起点经纬度坐标
- `destination`: 终点经纬度坐标

## 6. maps_direction_walking
步行路径规划 API 可以根据输入起点终点经纬度坐标规划100km 以内的步行通勤方案，并且返回通勤方案的数据

**参数：**
- `origin`: 起点经纬度坐标
- `destination`: 终点经纬度坐标

## 7. maps_direction_driving
驾车路径规划 API 可以根据用户起终点经纬度坐标规划以小客车、轿车通勤出行的方案，并且返回通勤方案的数据

**参数：**
- `origin`: 起点经纬度坐标
- `destination`: 终点经纬度坐标

## 8. maps_direction_transit_integrated
根据用户起终点经纬度坐标规划综合各类公共（火车、公交、地铁）交通方式的通勤方案，并且返回通勤方案的数据，跨城场景下必须传起点城市与终点城市

**参数：**
- `origin`: 起点经纬度坐标
- `destination`: 终点经纬度坐标
- `city`: 起点城市
- `cityd`: 终点城市

## 9. maps_distance
测量两个经纬度坐标之间的距离,支持驾车、步行以及球面距离测量

**参数：**
- `origins`: 起点经纬度坐标
- `destination`: 终点经纬度坐标
- `type` (可选，默认为"1"): 测量类型

## 10. maps_text_search
关键词搜索 API 根据用户输入的关键字进行 POI 搜索，并返回相关的信息

**参数：**
- `keywords`: 搜索关键词
- `city` (可选): 查询城市
- `citylimit` (可选，默认为"false"): 是否限制城市范围内搜索

## 11. maps_around_search
周边搜，根据用户传入关键词以及坐标location，搜索出radius半径范围的POI

**参数：**
- `location`: 中心点经纬度坐标
- `radius` (可选，默认为"1000"): 搜索半径
- `keywords` (可选): 搜索关键词

## 12. maps_search_detail
查询关键词搜或者周边搜获取到的POI ID的详细信息

**参数：**
- `id`: POI ID

# 配置方法

要使用此服务，您需要在应用中添加以下MCP配置：

```json
{
    "mcpServers": {
        "amap-mcp-server": {
            "command": "uvx",
            "args": [
                "amap-mcp-server"
            ],
            "env": {
                "AMAP_MAPS_API_KEY": "your valid amap maps api key"
            }
        }
    }
}
```

将上述配置添加到您的配置文件中，并确保将`"your valid amap maps api key"`替换为您的实际高德地图API密钥。您可以在[高德开放平台](https://lbs.amap.com/)注册并获取API密钥。


