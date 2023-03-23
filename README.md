# Battery Module 
This is a spin-off from https://github.com/hoelzro/linux-fake-battery-module to make a kernel module and supporting OS service for raspberry pi (and other) systems to integrate with power supplies using the max1704x li-ion monitoring chip, like the Amp Ripper 4000 [Kickstarter Link](https://www.kickstarter.com/projects/ksd/ampripper-4000-next-gen-battery-charger-and-boost-module).  It should be totally possible to add support for the ads1015, used by the Retro PSU, and other chips.

The kernel module creates a virtual battery in linux that is reported like a laptop battery on the taskbar, etc.  We run a service that queries the max1704x chip over i2c and relays the battery percent and charging status to the kernel module.

<img src="/images/battery_status.png" alt="Taskbar Battery" width="430"/>

I tried using the kernel module on Raspberry Pi OS, and it works but the Lxde window manager seems to crash when it sees a battery.  So I'm using this with Ubuntu 22.10 on a Pi 4 and it's working perfectly.

Feedback and contributions are welcome here.

## Wiring and software setup:
There are a few steps to set this up.  I check out the repo and run everything from the checkout dir, so there's no installer, just a some manual steps to enable it.

### 1 - Wiring the power supply to the pi and enabling i2c:
Here's a wiring diagram for the Amp Ripper 4K. All that's needed are the i2c wires.  A 3rd wire can be added to the INT pin to trigger shutdown on low voltage if desired.  The max1704x is configurable per the voltage this happens at.

<img src="/images/ar_pi_wiring.png" alt="ark wiring diagram" width="600"/>

If you're on Raspberry Pi OS, you'll need to enable i2c (e.g. with raspi-config).  More info at https://github.com/fivdi/i2c-bus/blob/master/doc/raspberry-pi-i2c.md

Once attached, you can use i2cdetect to verify the pi can see the max1704x over i2c. Look for the "36" device for the max1704x: 

    $ sudo apt install i2c-tools
    $ sudo  usermod -a -G dialout dan 
    $ sudo reboot
    $ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
     00:                         -- -- -- -- -- -- -- -- 
     10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
     20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
     30: -- -- -- -- -- -- 36 -- -- -- -- -- -- -- -- -- 
     40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

    
If you used different i2c pins on your pi, you might need to check available i2c bus devices with i2cdetect -l and query them instead.  I'm not sure offhand how this will affect the battery_update.pi.  Mihgt need to change an i2c addr in there.

### 2 - Build the module and test it:
On Ubuntu, all of the needed packages were installed already, but on Raspberry pi OS, I needed to install a few packages:

    $ sudo apt install git bc bison flex libssl-dev make raspberrypi-kernel-headers

The Clone the repo and "make" the module:

    $ cd rpi-integrated-battery-module
    $ make

You should now see integrated_battery.ko listed.

### 3 - Test and install the service
Update the paths to the rpi-integrated-battery-module in the following files/lines:

    ./battery_update.py:MODULE = '/home/dan/git/rpi-integrated-battery-module/integrated_battery.ko'
    ./battery_update.py:STATUS_FILE = '/home/dan/git/rpi-integrated-battery-module/status.log'
    ./battery_update.service:WorkingDirectory=/home/dan/git/rpi-integrated-battery-module/
    ./battery_update.service:ExecStart=/home/dan/git/rpi-integrated-battery-module/battery_update.py

And install a couple needed packages and try running the script to check for errors:

    $ sudo apt install python3-pip python3-rpi.gpio
    $ sudo pip3 install adafruit-circuitpython-max1704x
    $ sudo ./battery_update.py

Add a symlink for the service, try starting it, and enable it to run at boot:

    $ sudo ln -s /home/dan/git/rpi-integrated-battery-module/battery_update.service /etc/systemd/system/battery_update.service
    $ sudo systemctl start battery_update.service
    $ sudo systemctl status battery_update.service
    $ sudo systemctl enable battery_update.service
    
If you see an error from the status command, try running battery_update.py manually and fix any issues reported.

## More info on how this works

The kernel module created a character device at /dev/integrated_battery.  The service reads charge level over i2c from the battery monitor chip and passes the battery percent and charging status to the kernel module.  You can test this manually by echoing values to the module:

    $ sudo echo "charging = 0 > /dev/integrated_battery" # set the state to discharging
    $ sudo echo "charging = 1 > /dev/integrated_battery" # set the state to charging
    $ sudo echo "capacity0 = 75 > /dev/integrated_battery" # set the battery percent to 75


