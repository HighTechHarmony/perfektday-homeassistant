# PERFEKTday HomeAssistant Script

## Periodically sends color tuning commands to a group of Philips Hue bulbs throughout the day

This can be useful as a bio-coordinated lighting approach, such as Circadian Lighting

## Dependencies

HomeAssistant "Python Scripts" integration
For more info, see: https://www.home-assistant.io/integrations/python_script/

## Usage

- Copy perfektday_v2.py into /homeassistant/python_scripts
- Create a Zigbee group(s) of Philips Hue bulbs you wish to control
- Create an automation with your specific time and color conditions as follows (excerpt contains example data):

```
alias: PERFEKTday_all
description: PERFEKTday
mode: single
triggers:
  - seconds: /12
    trigger: time_pattern
conditions: []
actions:
  - data:
      entity_id:
        - light.perfektday_group_livingroom_hue_zha_group_0x0005
        - light.signify_netherlands_b_v_lta008_huelight
        - light.perfektday_group_perfektday_group_zha_group_0x0002
        - light.signify_netherlands_b_v_lta008_huelight_2
      min_color_temp: 2700
      max_color_temp: 6500
      sunup: 6
      solarnoon: 1
      sundown: 17
      brightness: 255
    action: python_script.perfektday_v2
```

- Replace the entity_ids with your bulb(s) or group(s)
- Adjust your update frequency as desired, but it should probably be fairly frequent (<30 seconds),
  as lights turning on will take that long, at maximum, to receive a color update
