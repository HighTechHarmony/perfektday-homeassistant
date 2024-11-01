# Title: PERFEKTday 
# Description: this script periodically sends color tuning commands to a group of Philips Hue bulbs throughout the day
# This can be useful as a bio-coordinated lighting approach, such as Circadian Lighting
# Original Author: Scott McGrath (scott@smcgrath.com)

# Usage:
# Create an automation with your specific time and color conditions as follows.  
# Adjust your update frequency as desired, but it should probably be fairly frequent (<30 seconds), 
# as lights turning on will take that long, at maximum, to receive a color update

# alias: PERFEKTday_all
# description: PERFEKTday
# mode: single
# triggers:
#   - seconds: /12
#     trigger: time_pattern
# conditions: []
# actions:
#   - data:
#       entity_id:
#         - light.perfektday_group_livingroom_hue_zha_group_0x0005
#         - light.signify_netherlands_b_v_lta008_huelight
#         - light.perfektday_group_perfektday_group_zha_group_0x0002
#         - light.signify_netherlands_b_v_lta008_huelight_2
#       min_color_temp: 2700
#       max_color_temp: 6500
#       sunup: 6
#       solarnoon: 1
#       sundown: 17
#       brightness: 255
#     action: python_script.perfektday_v2


# turn_on_light.py
entity_id = data.get("entity_id")
#color_temp = data.get("color_temp", [250])
brightness = data.get("brightness", [255])
max_color_temp = data.get ('max_color_temp', [6500])
min_color_temp = data.get ('min_color_temp', [2700])
SunUp = data.get ("sunup")
SolarNoon = data.get ("solarnoon")
SunDown = data.get ("sundown")


def CCTPerfektDay(minsnow):
    # return 6500
    #    Returns cct in kelvin based on given minutes, uses globals SunUp, SunDown, SolarNoon, min_color_temp and max_color_temp
    
    sunup = TimeToMins( int(SunUp))
    sundown = TimeToMins( int(SunDown))
    sonoon = TimeToMins( int(SolarNoon))


    if minsnow < sunup or minsnow > sundown:  # night
        return min_color_temp  # Night setting, min CCT
    if minsnow >= sunup and minsnow < sonoon:  # pre-noon
        return (min_color_temp + (math.sin((float(minsnow - sunup) / float(sonoon - sunup)) * (3.1416/2))) * (max_color_temp - min_color_temp))  # CCT sin scaled
    if minsnow <= sundown and minsnow >= sonoon:  # noon / post-noon
        return (min_color_temp + (math.sin((float(sundown - minsnow) / float(sundown - sonoon)) * (3.1416/2))) * (max_color_temp - min_color_temp))  # CCT sin scaled
        

def minutes_since_midnight():
    t = time.localtime()
    return int(t.tm_hour) * 60 + int(t.tm_min)
    

def TimeToMins(thesehours):
    return int(60*thesehours)
    
def clamp(value, minimum, maximum):
    return max(min(value, maximum), minimum)
    
def kelvin_to_mired(kelvin):
    mired = 1000000 / kelvin
    return mired

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)    
    
def approx_sin(x):
    #    Approximates the value of sin(x) using a lookup table
    sin_table = {}
    
    sin_table[0] = 0.0
    sin_table[18] = 0.3090169943749474
    sin_table[36] = 0.5877852522924731
    sin_table[54] = 0.8090169943749473
    sin_table[72] = 0.9510565162951535
    sin_table[90] = 1.0
    sin_table[108] = 0.9510565162951535
    sin_table[126] = 0.8090169943749475
    sin_table[144] = 0.5877852522924732
    sin_table[162] = 0.30901699437494773
    sin_table[180] = 1.2246467991473532e-16
    sin_table[198] = -0.30901699437494723
    sin_table[216] = -0.587785252292473
    sin_table[234] = -0.8090169943749473
    sin_table[252] = -0.9510565162951535
    sin_table[270] = -1.0
    sin_table[288] = -0.9510565162951536
    sin_table[306] = -0.8090169943749476
    sin_table[324] = -0.5877852522924734
    sin_table[342] = -0.30901699437494795
    x =  radians_to_degrees (x)
    x = x % 360
    key = min(sin_table.keys(), key=lambda k: abs(k-x))
    return sin_table[key]

def radians_to_degrees(radians):
    return radians * 180 / 3.141592653589793    
    

# logger.info("In perfektday.py")
# Compute cct_now

# logger.info(CCTPerfektDay(minutes_since_midnight()))
cct_now_mired = kelvin_to_mired(CCTPerfektDay(minutes_since_midnight()))
# cct_now_mired = kelvin_to_mired(CCTPerfektDay(10*60))

# Command the entities specified individually
if entity_id is not None:
    for entity in entity_id:
        # service_data = {"entity_id": entity, "color_temp": cct_now_mired, "brightness": brightness, "transition": 3}
        service_data = {"entity_id": entity, "color_temp": cct_now_mired, "transition": 3}
        
        # Below line avoids changing the color of a bulb unless it's on, but it won't work with a large group of bulbs in unknown states
        if hass.states.get(entity).state is not "off":
            hass.services.call("light", "turn_on", service_data, False)
        

