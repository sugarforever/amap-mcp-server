from server import maps_regeocode

if __name__ == "__main__":
    response = maps_regeocode("116.410829,39.881913")
    print(response)