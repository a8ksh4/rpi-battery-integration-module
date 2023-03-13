# Battery Module 
This is a spin-off from https://github.com/hoelzro/linux-fake-battery-module to make a kernel module for raspberry pi systems to integrate with max1704x, ads1015, etc voltage monitoring boards and enable us to have our external batteries visible to standard linux power management like a laptop, so we can see a battery gauge in the task bar and take advantage of any power management features.

So short term goals are this:
* Reduce the module to only having 1 batteryrather than 2
* Get module loading and reporting on current 4.9 kernel in Raspberry Pi OS.
* Implement simple OS service with some python code to query the battery reporting module and pass updates to the kernel module.
* Work out specifics needed to get a battery gauge to show up on the task bar in RPi OS.

## Installing the service and building the module
    $ sudo apt install git bc bison flex libssl-dev make raspberrypi-kernel-headers
    $ cd rpi-battery-integration-module
    # make
    # 

## Loading the module

You can build the module with a simple `make`, and load it with `insmod`:

    $ sudo insmod ./fake_battery.ko

## Changing battery values via /dev/fake\_battery

You can write values to `/dev/fake_battery` to change the current charging/discharging
and charge levels of the battery:

    $ echo 'charging = 0' | sudo tee /dev/fake_battery # set state to discharging
    $ echo 'charging = 1' | sudo tee /dev/fake_battery # set state to charging
    $ echo 'capacity0 = 77' | sudo tee /dev/fake_battery # set charge on BAT0 to 77%
    $ echo 'capacity1 = 77' | sudo tee /dev/fake_battery # set charge on BAT1 to 77%

