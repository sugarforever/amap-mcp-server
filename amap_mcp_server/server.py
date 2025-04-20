import os
from typing import Any, Dict, List, Optional
import requests
from mcp.server.fastmcp import FastMCP

def get_api_key() -> str:
    """Get the Amap Maps API key from environment variables"""
    api_key = os.getenv("AMAP_MAPS_API_KEY")
    if not api_key:
        raise ValueError("AMAP_MAPS_API_KEY environment variable is required")
    return api_key

AMAP_MAPS_API_KEY = get_api_key()

mcp = FastMCP("amap-maps")

@mcp.tool()
def maps_regeocode(location: str) -> Dict[str, Any]:
    """将一个高德经纬度坐标转换为行政区划地址信息"""
    try:
        response = requests.get(
            "https://restapi.amap.com/v3/geocode/regeo",
            params={
                "key": AMAP_MAPS_API_KEY,
                "location": location
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"RGeocoding failed: {data.get('info') or data.get('infocode')}"}
            
        return {
            "province": data["regeocode"]["addressComponent"]["province"],
            "city": data["regeocode"]["addressComponent"]["city"],
            "district": data["regeocode"]["addressComponent"]["district"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def maps_geo(address: str, city: Optional[str] = None) -> Dict[str, Any]:
    """将详细的结构化地址转换为经纬度坐标。支持对地标性名胜景区、建筑物名称解析为经纬度坐标"""
    try:
        params = {
            "key": AMAP_MAPS_API_KEY,
            "address": address
        }
        if city:
            params["city"] = city
            
        response = requests.get(
            "https://restapi.amap.com/v3/geocode/geo",
            params=params
        )
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"Geocoding failed: {data.get('info') or data.get('infocode')}"}
            
        geocodes = data.get("geocodes", [])
        results = []
        for geo in geocodes:
            results.append({
                "country": geo.get("country"),
                "province": geo.get("province"),
                "city": geo.get("city"),
                "citycode": geo.get("citycode"),
                "district": geo.get("district"),
                "street": geo.get("street"),
                "number": geo.get("number"),
                "adcode": geo.get("adcode"),
                "location": geo.get("location"),
                "level": geo.get("level")
            })
        return {"return": results}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def maps_ip_location(ip: str) -> Dict[str, Any]:
    """IP 定位根据用户输入的 IP 地址，定位 IP 的所在位置"""
    try:
        response = requests.get(
            "https://restapi.amap.com/v3/ip",
            params={
                "key": AMAP_MAPS_API_KEY,
                "ip": ip
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"IP Location failed: {data.get('info') or data.get('infocode')}"}
            
        return {
            "province": data.get("province"),
            "city": data.get("city"),
            "adcode": data.get("adcode"),
            "rectangle": data.get("rectangle")
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def maps_weather(city: str) -> Dict[str, Any]:
    """根据城市名称或者标准adcode查询指定城市的天气"""
    try:
        response = requests.get(
            "https://restapi.amap.com/v3/weather/weatherInfo",
            params={
                "key": AMAP_MAPS_API_KEY,
                "city": city,
                "extensions": "all"
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"Get weather failed: {data.get('info') or data.get('infocode')}"}
            
        forecasts = data.get("forecasts", [])
        if not forecasts:
            return {"error": "No forecast data available"}
            
        return {
            "city": forecasts[0]["city"],
            "forecasts": forecasts[0]["casts"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def maps_bicycling(origin: str, destination: str) -> Dict[str, Any]:
    """骑行路径规划用于规划骑行通勤方案，规划时会考虑天桥、单行线、封路等情况。最大支持 500km 的骑行路线规划"""
    try:
        response = requests.get(
            "https://restapi.amap.com/v4/direction/bicycling",
            params={
                "key": AMAP_MAPS_API_KEY,
                "origin": origin,
                "destination": destination
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get("errcode") != 0:
            return {"error": f"Direction bicycling failed: {data.get('info') or data.get('infocode')}"}
            
        paths = []
        for path in data["data"]["paths"]:
            steps = []
            for step in path["steps"]:
                steps.append({
                    "instruction": step.get("instruction"),
                    "road": step.get("road"),
                    "distance": step.get("distance"),
                    "orientation": step.get("orientation"),
                    "duration": step.get("duration")
                })
            paths.append({
                "distance": path.get("distance"),
                "duration": path.get("duration"),
                "steps": steps
            })
            
        return {
            "data": {
                "origin": data["data"]["origin"],
                "destination": data["data"]["destination"],
                "paths": paths
            }
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def maps_direction_walking(origin: str, destination: str) -> Dict[str, Any]:
    """步行路径规划 API 可以根据输入起点终点经纬度坐标规划100km 以内的步行通勤方案，并且返回通勤方案的数据"""
    try:
        response = requests.get(
            "https://restapi.amap.com/v3/direction/walking",
            params={
                "key": AMAP_MAPS_API_KEY,
                "origin": origin,
                "destination": destination
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"Direction Walking failed: {data.get('info') or data.get('infocode')}"}
            
        paths = []
        for path in data["route"]["paths"]:
            steps = []
            for step in path["steps"]:
                steps.append({
                    "instruction": step.get("instruction"),
                    "road": step.get("road"),
                    "distance": step.get("distance"),
                    "orientation": step.get("orientation"),
                    "duration": step.get("duration")
                })
            paths.append({
                "distance": path.get("distance"),
                "duration": path.get("duration"),
                "steps": steps
            })
            
        return {
            "route": {
                "origin": data["route"]["origin"],
                "destination": data["route"]["destination"],
                "paths": paths
            }
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def maps_direction_driving(origin: str, destination: str) -> Dict[str, Any]:
    """驾车路径规划 API 可以根据用户起终点经纬度坐标规划以小客车、轿车通勤出行的方案，并且返回通勤方案的数据"""
    try:
        response = requests.get(
            "https://restapi.amap.com/v3/direction/driving",
            params={
                "key": AMAP_MAPS_API_KEY,
                "origin": origin,
                "destination": destination
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"Direction Driving failed: {data.get('info') or data.get('infocode')}"}
            
        paths = []
        for path in data["route"]["paths"]:
            steps = []
            for step in path["steps"]:
                steps.append({
                    "instruction": step.get("instruction"),
                    "road": step.get("road"),
                    "distance": step.get("distance"),
                    "orientation": step.get("orientation"),
                    "duration": step.get("duration")
                })
            paths.append({
                "path": path.get("path"),
                "distance": path.get("distance"),
                "duration": path.get("duration"),
                "steps": steps
            })
            
        return {
            "route": {
                "origin": data["route"]["origin"],
                "destination": data["route"]["destination"],
                "paths": paths
            }
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def maps_direction_transit_integrated(origin: str, destination: str, city: str, cityd: str) -> Dict[str, Any]:
    """根据用户起终点经纬度坐标规划综合各类公共（火车、公交、地铁）交通方式的通勤方案，并且返回通勤方案的数据，跨城场景下必须传起点城市与终点城市"""
    try:
        response = requests.get(
            "https://restapi.amap.com/v3/direction/transit/integrated",
            params={
                "key": AMAP_MAPS_API_KEY,
                "origin": origin,
                "destination": destination,
                "city": city,
                "cityd": cityd
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"Direction Transit Integrated failed: {data.get('info') or data.get('infocode')}"}
            
        transits = []
        if data["route"].get("transits"):
            for transit in data["route"]["transits"]:
                segments = []
                if transit.get("segments"):
                    for segment in transit["segments"]:
                        walking_steps = []
                        if segment.get("walking", {}).get("steps"):
                            for step in segment["walking"]["steps"]:
                                walking_steps.append({
                                    "instruction": step.get("instruction"),
                                    "road": step.get("road"),
                                    "distance": step.get("distance"),
                                    "action": step.get("action"),
                                    "assistant_action": step.get("assistant_action")
                                })
                                
                        buslines = []
                        if segment.get("bus", {}).get("buslines"):
                            for busline in segment["bus"]["buslines"]:
                                via_stops = []
                                if busline.get("via_stops"):
                                    for stop in busline["via_stops"]:
                                        via_stops.append({"name": stop.get("name")})
                                        
                                buslines.append({
                                    "name": busline.get("name"),
                                    "departure_stop": {"name": busline.get("departure_stop", {}).get("name")},
                                    "arrival_stop": {"name": busline.get("arrival_stop", {}).get("name")},
                                    "distance": busline.get("distance"),
                                    "duration": busline.get("duration"),
                                    "via_stops": via_stops
                                })
                                
                        segments.append({
                            "walking": {
                                "origin": segment.get("walking", {}).get("origin"),
                                "destination": segment.get("walking", {}).get("destination"),
                                "distance": segment.get("walking", {}).get("distance"),
                                "duration": segment.get("walking", {}).get("duration"),
                                "steps": walking_steps
                            },
                            "bus": {"buslines": buslines},
                            "entrance": {"name": segment.get("entrance", {}).get("name")},
                            "exit": {"name": segment.get("exit", {}).get("name")},
                            "railway": {
                                "name": segment.get("railway", {}).get("name"),
                                "trip": segment.get("railway", {}).get("trip")
                            }
                        })
                        
                transits.append({
                    "duration": transit.get("duration"),
                    "walking_distance": transit.get("walking_distance"),
                    "segments": segments
                })
                
        return {
            "route": {
                "origin": data["route"]["origin"],
                "destination": data["route"]["destination"],
                "distance": data["route"].get("distance"),
                "transits": transits
            }
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def maps_distance(origins: str, destination: str, type: str = "1") -> Dict[str, Any]:
    """测量两个经纬度坐标之间的距离,支持驾车、步行以及球面距离测量"""
    try:
        response = requests.get(
            "https://restapi.amap.com/v3/distance",
            params={
                "key": AMAP_MAPS_API_KEY,
                "origins": origins,
                "destination": destination,
                "type": type
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"Direction Distance failed: {data.get('info') or data.get('infocode')}"}
            
        results = []
        for result in data["results"]:
            results.append({
                "origin_id": result.get("origin_id"),
                "dest_id": result.get("dest_id"),
                "distance": result.get("distance"),
                "duration": result.get("duration")
            })
            
        return {"results": results}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def maps_text_search(keywords: str, city: str = "", citylimit: str = "false") -> Dict[str, Any]:
    """关键词搜索 API 根据用户输入的关键字进行 POI 搜索，并返回相关的信息"""
    try:
        response = requests.get(
            "https://restapi.amap.com/v3/place/text",
            params={
                "key": AMAP_MAPS_API_KEY,
                "keywords": keywords,
                "city": city,
                "citylimit": citylimit
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"Text Search failed: {data.get('info') or data.get('infocode')}"}
            
        suggestion_cities = []
        if data.get("suggestion", {}).get("cities"):
            for city in data["suggestion"]["cities"]:
                suggestion_cities.append({"name": city.get("name")})
                
        pois = []
        for poi in data.get("pois", []):
            pois.append({
                "id": poi.get("id"),
                "name": poi.get("name"),
                "address": poi.get("address"),
                "typecode": poi.get("typecode")
            })
            
        return {
            "suggestion": {
                "keywords": data.get("suggestion", {}).get("keywords"),
                "cities": suggestion_cities
            },
            "pois": pois
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def maps_around_search(location: str, radius: str = "1000", keywords: str = "") -> Dict[str, Any]:
    """周边搜，根据用户传入关键词以及坐标location，搜索出radius半径范围的POI"""
    try:
        response = requests.get(
            "https://restapi.amap.com/v3/place/around",
            params={
                "key": AMAP_MAPS_API_KEY,
                "location": location,
                "radius": radius,
                "keywords": keywords
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"Around Search failed: {data.get('info') or data.get('infocode')}"}
            
        pois = []
        for poi in data.get("pois", []):
            pois.append({
                "id": poi.get("id"),
                "name": poi.get("name"),
                "address": poi.get("address"),
                "typecode": poi.get("typecode")
            })
            
        return {"pois": pois}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def maps_search_detail(id: str) -> Dict[str, Any]:
    """查询关键词搜或者周边搜获取到的POI ID的详细信息"""
    try:
        response = requests.get(
            "https://restapi.amap.com/v3/place/detail",
            params={
                "key": AMAP_MAPS_API_KEY,
                "id": id
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"Get poi detail failed: {data.get('info') or data.get('infocode')}"}
            
        if not data.get("pois"):
            return {"error": "No POI found"}
            
        poi = data["pois"][0]
        result = {
            "id": poi.get("id"),
            "name": poi.get("name"),
            "location": poi.get("location"),
            "address": poi.get("address"),
            "business_area": poi.get("business_area"),
            "city": poi.get("cityname"),
            "type": poi.get("type"),
            "alias": poi.get("alias")
        }
        
        # Add biz_ext data if available
        if poi.get("biz_ext"):
            result.update(poi["biz_ext"])
            
        return result
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

if __name__ == "__main__":
    mcp.run()