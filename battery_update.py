#!/usr/bin/env python3

import os
import time
import board
import adafruit_max1704x

if __name__ == '__main__':
    i2c = board.I2C()
    max17 = adafruit_max1704x.MAX17048(i2c)
    
    max17.wake()
    max17.voltage_alert_min = 3.5
    max17.voltage_alert_max = 4.1
    print("Voltage alert minimum = %0.2f V" % max17.voltage_alert_min)
    print("Voltage alert maximum = %0.2f V" % max17.voltage_alert_max)
    
    while True:
        time.sleep(15)
        print()
        print(f'Cell Voltage: {max17.cell_voltage:.2f} Volts')
        print(f'Cell Percent: {max17.cell_percent:.1f} %')
        print('Charge Rate:', max17.charge_rate)
        if os.path.exists('/dev/integrated_battery'):
            print('updating battery')
            charging_status = 1 if max17.charge_rate > 0 else 0
            try:
                with open('/dev/integrated_battery', 'w') as f:
                    f.write(f'capacity0 = {int(max17.cell_percent)}\n')
                with open('/dev/integrated_battery', 'w') as f:
                    f.write(f'charging = {charging_status}\n')
            except Exception as e:
                print("exceptin", e)
    
        # if max17.hibernating:
        #     print("Hibernating!")
    
        # if max17.active_alert:
        #     print("Alert!")
        #     if max17.reset_alert:
        #         print("  Reset indicator")
        #         max17.reset_alert = False  # clear the alert
    
        #     if max17.voltage_high_alert:
        #         print("  Voltage high")
        #         max17.voltage_high_alert = False  # clear the alert
    
        #     if max17.voltage_low_alert:
        #         print("  Voltage low")
        #         max17.voltage_low_alert = False  # clear the alert
    
        #     if max17.voltage_reset_alert:
        #         print("  Voltage reset")
        #         max17.voltage_reset_alert = False  # clear the alert
    
        #     if max17.SOC_low_alert:
        #         print("  Charge low")
        #         max17.SOC_low_alert = False  # clear the alert
    
        #     if max17.SOC_change_alert:
        #         print("  Charge changed")
        #         max17.SOC_change_alert = False  # clear the alert
    
