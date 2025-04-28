# 高德地图 MCP Server

该高德地图 MCP Server 发布在 [PyPI](https://pypi.org/project/amap-mcp-server/)。

## MCP 工具列表

本服务提供以下工具：

### 地理编码工具

#### maps_regeocode
将一个高德经纬度坐标转换为行政区划地址信息

**参数：**
- `location`: 经纬度坐标

#### maps_geo
将详细的结构化地址转换为经纬度坐标。支持对地标性名胜景区、建筑物名称解析为经纬度坐标

**参数：**
- `address`: 结构化地址
- `city` (可选): 指定查询的城市

### 位置服务工具

#### maps_ip_location
IP 定位根据用户输入的 IP 地址，定位 IP 的所在位置

**参数：**
- `ip`: IP地址

#### maps_weather
根据城市名称或者标准adcode查询指定城市的天气

**参数：**
- `city`: 城市名称或者adcode

### 路线规划工具

#### 骑行路线
##### maps_bicycling_by_coordinates
骑行路径规划用于规划骑行通勤方案，规划时会考虑天桥、单行线、封路等情况。最大支持 500km 的骑行路线规划

**参数：**
- `origin`: 起点经纬度坐标
- `destination`: 终点经纬度坐标

##### maps_bicycling_by_address
骑行路径规划（地址版），使用地址进行骑行路线规划，推荐优先使用此工具

**参数：**
- `origin_address`: 起点地址（例如："北京市朝阳区阜通东大街6号"）
- `destination_address`: 终点地址（例如："北京市海淀区上地十街10号"）
- `origin_city` (可选): 起点所在城市，用于提高地理编码准确性
- `destination_city` (可选): 终点所在城市，用于提高地理编码准确性

#### 步行路线
##### maps_direction_walking_by_coordinates
步行路径规划 API 可以根据输入起点终点经纬度坐标规划100km 以内的步行通勤方案，并且返回通勤方案的数据

**参数：**
- `origin`: 起点经纬度坐标
- `destination`: 终点经纬度坐标

##### maps_direction_walking_by_address
步行路径规划（地址版），使用地址进行步行路线规划，推荐优先使用此工具

**参数：**
- `origin_address`: 起点地址（例如："北京市朝阳区阜通东大街6号"）
- `destination_address`: 终点地址（例如："北京市海淀区上地十街10号"）
- `origin_city` (可选): 起点所在城市，用于提高地理编码准确性
- `destination_city` (可选): 终点所在城市，用于提高地理编码准确性

#### 驾车路线
##### maps_direction_driving_by_coordinates
驾车路径规划 API 可以根据用户起终点经纬度坐标规划以小客车、轿车通勤出行的方案，并且返回通勤方案的数据

**参数：**
- `origin`: 起点经纬度坐标
- `destination`: 终点经纬度坐标

##### maps_direction_driving_by_address
驾车路径规划（地址版），使用地址进行驾车路线规划，推荐优先使用此工具

**参数：**
- `origin_address`: 起点地址（例如："北京市朝阳区阜通东大街6号"）
- `destination_address`: 终点地址（例如："北京市海淀区上地十街10号"）
- `origin_city` (可选): 起点所在城市，用于提高地理编码准确性
- `destination_city` (可选): 终点所在城市，用于提高地理编码准确性

#### 公共交通路线
##### maps_direction_transit_integrated_by_coordinates
根据用户起终点经纬度坐标规划综合各类公共（火车、公交、地铁）交通方式的通勤方案，并且返回通勤方案的数据，跨城场景下必须传起点城市与终点城市

**参数：**
- `origin`: 起点经纬度坐标
- `destination`: 终点经纬度坐标
- `city`: 起点城市
- `cityd`: 终点城市

##### maps_direction_transit_integrated_by_address
公共交通路径规划（地址版），使用地址进行公共交通路线规划，推荐优先使用此工具

**参数：**
- `origin_address`: 起点地址（例如："北京市朝阳区阜通东大街6号"）
- `destination_address`: 终点地址（例如："北京市海淀区上地十街10号"）
- `origin_city`: 起点所在城市（跨城交通必需）
- `destination_city`: 终点所在城市（跨城交通必需）

### 距离测量工具

#### maps_distance
测量两个经纬度坐标之间的距离,支持驾车、步行以及球面距离测量

**参数：**
- `origins`: 起点经纬度坐标
- `destination`: 终点经纬度坐标
- `type` (可选，默认为"1"): 测量类型

### POI搜索工具

#### maps_text_search
关键词搜索 API 根据用户输入的关键字进行 POI 搜索，并返回相关的信息

**参数：**
- `keywords`: 搜索关键词
- `city` (可选): 查询城市
- `citylimit` (可选，默认为"false"): 是否限制城市范围内搜索

#### maps_around_search
周边搜，根据用户传入关键词以及坐标location，搜索出radius半径范围的POI

**参数：**
- `location`: 中心点经纬度坐标
- `radius` (可选，默认为"1000"): 搜索半径
- `keywords` (可选): 搜索关键词

#### maps_search_detail
查询关键词搜或者周边搜获取到的POI ID的详细信息

**参数：**
- `id`: POI ID

## 配置方法

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


