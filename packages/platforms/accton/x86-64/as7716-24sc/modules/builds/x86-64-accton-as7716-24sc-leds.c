/*
 * A LED driver for the as7716_24sc_led
 *
 * Copyright (C) 2014 Accton Technology Corporation.
 * Brandon Chuang <brandon_chuang@accton.com.tw>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

/*#define DEBUG*/ 

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/platform_device.h>
#include <linux/err.h>
#include <linux/leds.h>
#include <linux/slab.h>
#include <linux/dmi.h>

extern int accton_i2c_cpld_read (unsigned short cpld_addr, u8 reg);
extern int accton_i2c_cpld_write(unsigned short cpld_addr, u8 reg, u8 value);

#define DRVNAME "as7716_24sc_led"

struct as7716_24sc_led_data {
	struct platform_device *pdev;
	struct mutex	 update_lock;
	char			 valid;		   /* != 0 if registers are valid */
	unsigned long	last_updated;	/* In jiffies */
	u8			   reg_val[1];	  /* only 1 register*/
};

static struct as7716_24sc_led_data  *ledctl = NULL;

/* LED related data
 */

#define LED_CNTRLER_I2C_ADDRESS		(0x60)
 
#define LED_TYPE_DIAG_REG_MASK	 	(0x03)
#define LED_MODE_DIAG_YELLOW_VALUE  (0x00)
#define LED_MODE_DIAG_ORANGE_VALUE	(0x01)
#define LED_MODE_DIAG_GREEN_VALUE  	(0x02)
#define LED_MODE_DIAG_OFF_VALUE		(0x03)

#define LED_TYPE_LOC_REG_MASK	 	(0x10)
#define LED_MODE_LOC_ORANGE_VALUE	(0x00)
#define LED_MODE_LOC_OFF_VALUE		(0x10)

enum led_type {
	LED_TYPE_DIAG,
	LED_TYPE_LOC,
	LED_TYPE_FAN,
	LED_TYPE_PSU1,
	LED_TYPE_PSU2
};

struct led_reg {
	u32  types;
	u8   reg_addr;
};

static const struct led_reg led_reg_map[] = {
	{(1 << LED_TYPE_LOC) | (1 << LED_TYPE_DIAG) | (1 << LED_TYPE_FAN), 0x30},
};

enum led_light_mode {
    LED_MODE_OFF,
    LED_MODE_RED 				= 10,
    LED_MODE_RED_BLINKING 		= 11,
    LED_MODE_ORANGE 			= 12,
    LED_MODE_ORANGE_BLINKING 	= 13,
    LED_MODE_YELLOW 			= 14,
    LED_MODE_YELLOW_BLINKING 	= 15,
    LED_MODE_GREEN 				= 16,
    LED_MODE_GREEN_BLINKING 	= 17,
    LED_MODE_BLUE 				= 18,
    LED_MODE_BLUE_BLINKING 		= 19,
    LED_MODE_PURPLE 			= 20,
    LED_MODE_PURPLE_BLINKING 	= 21,
    LED_MODE_AUTO 				= 22,
    LED_MODE_AUTO_BLINKING 		= 23,
    LED_MODE_WHITE 				= 24,
    LED_MODE_WHITE_BLINKING 	= 25,
    LED_MODE_CYAN 				= 26,
    LED_MODE_CYAN_BLINKING 		= 27,
    LED_MODE_UNKNOWN			= 99
};

struct led_type_mode {
	enum led_type type;
	enum led_light_mode mode;	
	int  reg_bit_mask;
	int  mode_value;
};

static struct led_type_mode led_type_mode_data[] = {
{LED_TYPE_LOC,  LED_MODE_OFF,	LED_TYPE_LOC_REG_MASK,  LED_MODE_LOC_OFF_VALUE},
{LED_TYPE_LOC,  LED_MODE_ORANGE,LED_TYPE_LOC_REG_MASK,  LED_MODE_LOC_ORANGE_VALUE},
{LED_TYPE_DIAG, LED_MODE_OFF,   LED_TYPE_DIAG_REG_MASK, LED_MODE_DIAG_OFF_VALUE},
{LED_TYPE_DIAG, LED_MODE_GREEN, LED_TYPE_DIAG_REG_MASK, LED_MODE_DIAG_GREEN_VALUE},
{LED_TYPE_DIAG, LED_MODE_ORANGE,LED_TYPE_DIAG_REG_MASK, LED_MODE_DIAG_ORANGE_VALUE},
{LED_TYPE_DIAG, LED_MODE_YELLOW,LED_TYPE_DIAG_REG_MASK, LED_MODE_DIAG_YELLOW_VALUE}
};
  
static int get_led_reg(enum led_type type, u8 *reg)
{	 
	int i;

	for (i = 0; i < ARRAY_SIZE(led_reg_map); i++) {	
		if(led_reg_map[i].types & (1 << type)) {
			*reg = led_reg_map[i].reg_addr;
			return 0;
		}
	}

	return 1;
}

static int led_reg_val_to_light_mode(enum led_type type, u8 reg_val) {
	int i;
	
	for (i = 0; i < ARRAY_SIZE(led_type_mode_data); i++) {

		if (type != led_type_mode_data[i].type)
			continue;
		   
		if ((led_type_mode_data[i].reg_bit_mask & reg_val) == 
			 led_type_mode_data[i].mode_value)
		{
			return led_type_mode_data[i].mode;
		}
	}
	
	return 0;
}

static u8 led_light_mode_to_reg_val(enum led_type type, 
									enum led_light_mode mode, u8 reg_val) {
	int i;
									  
	for (i = 0; i < ARRAY_SIZE(led_type_mode_data); i++) {
		if (type != led_type_mode_data[i].type)
			continue;

		if (mode != led_type_mode_data[i].mode)
			continue;

		reg_val = led_type_mode_data[i].mode_value | 
					 (reg_val & (~led_type_mode_data[i].reg_bit_mask));
		break;
	}
	
	return reg_val;
}

static int as7716_24sc_led_read_value(u8 reg)
{
	return accton_i2c_cpld_read(LED_CNTRLER_I2C_ADDRESS, reg);
}

static int as7716_24sc_led_write_value(u8 reg, u8 value)
{
	return accton_i2c_cpld_write(LED_CNTRLER_I2C_ADDRESS, reg, value);
}

static void as7716_24sc_led_update(void)
{
	mutex_lock(&ledctl->update_lock);

	if (time_after(jiffies, ledctl->last_updated + HZ + HZ / 2)
		|| !ledctl->valid) {
		int i;

		dev_dbg(&ledctl->pdev->dev, "Starting as7716_24sc_led update\n");

		/* Update LED data
		 */
		for (i = 0; i < ARRAY_SIZE(ledctl->reg_val); i++) {
			int status = as7716_24sc_led_read_value(led_reg_map[i].reg_addr);
			
			if (status < 0) {
				ledctl->valid = 0;
				dev_dbg(&ledctl->pdev->dev, "reg %d, err %d\n", led_reg_map[i].reg_addr, status);
				goto exit;
			}
			else
			{
				ledctl->reg_val[i] = status; 
			}
		}
		
		ledctl->last_updated = jiffies;
		ledctl->valid = 1;
	}
	
exit:	
	mutex_unlock(&ledctl->update_lock);
}

static void as7716_24sc_led_set(struct led_classdev *led_cdev,
									  enum led_brightness led_light_mode, 
									  enum led_type type)
{
	int reg_val;
	u8 reg	;
	mutex_lock(&ledctl->update_lock);

	if( !get_led_reg(type, &reg)) {
		dev_dbg(&ledctl->pdev->dev, "Not match register for %d.\n", type);
	}
	
	reg_val = as7716_24sc_led_read_value(reg);
	if (reg_val < 0) {
		dev_dbg(&ledctl->pdev->dev, "reg %d, err %d\n", reg, reg_val);
		goto exit;
	}

	reg_val = led_light_mode_to_reg_val(type, led_light_mode, reg_val);  
	as7716_24sc_led_write_value(reg, reg_val);

	/* to prevent the slow-update issue */
	ledctl->valid = 0;

exit:
	mutex_unlock(&ledctl->update_lock);
}


static void as7716_24sc_led_diag_set(struct led_classdev *led_cdev,
										   enum led_brightness led_light_mode)
{
	as7716_24sc_led_set(led_cdev, led_light_mode,  LED_TYPE_DIAG);
}

static enum led_brightness as7716_24sc_led_diag_get(struct led_classdev *cdev)
{
	as7716_24sc_led_update();
	return led_reg_val_to_light_mode(LED_TYPE_DIAG, ledctl->reg_val[0]);
}

static void as7716_24sc_led_loc_set(struct led_classdev *led_cdev,
										  enum led_brightness led_light_mode)
{
	as7716_24sc_led_set(led_cdev, led_light_mode, LED_TYPE_LOC);
}

static enum led_brightness as7716_24sc_led_loc_get(struct led_classdev *cdev)
{
	as7716_24sc_led_update();
	return led_reg_val_to_light_mode(LED_TYPE_LOC, ledctl->reg_val[0]);
}

static void as7716_24sc_led_auto_set(struct led_classdev *led_cdev,
										   enum led_brightness led_light_mode)
{
}

static enum led_brightness as7716_24sc_led_auto_get(struct led_classdev *cdev)
{
	return LED_MODE_AUTO;
}

static struct led_classdev as7716_24sc_leds[] = {
	[LED_TYPE_DIAG] = {
		.name			 = "as7716_24sc_led::diag",
		.default_trigger = "unused",
		.brightness_set	 = as7716_24sc_led_diag_set,
		.brightness_get	 = as7716_24sc_led_diag_get,
		.flags			 = LED_CORE_SUSPENDRESUME,
		.max_brightness	 = LED_MODE_GREEN,
	},
	[LED_TYPE_LOC] = {
		.name			 = "as7716_24sc_led::loc",
		.default_trigger = "unused",
		.brightness_set	 = as7716_24sc_led_loc_set,
		.brightness_get	 = as7716_24sc_led_loc_get,
		.flags			 = LED_CORE_SUSPENDRESUME,
		.max_brightness	 = LED_MODE_ORANGE,
	},
	[LED_TYPE_FAN] = {
		.name			 = "as7716_24sc_led::fan",
		.default_trigger = "unused",
		.brightness_set	 = as7716_24sc_led_auto_set,
		.brightness_get  = as7716_24sc_led_auto_get,
		.flags			 = LED_CORE_SUSPENDRESUME,
		.max_brightness  = LED_MODE_AUTO,
	},
	[LED_TYPE_PSU1] = {
		.name			 = "as7716_24sc_led::psu1",
		.default_trigger = "unused",
		.brightness_set	 = as7716_24sc_led_auto_set,
		.brightness_get  = as7716_24sc_led_auto_get,
		.flags			 = LED_CORE_SUSPENDRESUME,
		.max_brightness  = LED_MODE_AUTO,
	},
	[LED_TYPE_PSU2] = {
		.name			 = "as7716_24sc_led::psu2",
		.default_trigger = "unused",
		.brightness_set	 = as7716_24sc_led_auto_set,
		.brightness_get  = as7716_24sc_led_auto_get,
		.flags			 = LED_CORE_SUSPENDRESUME,
		.max_brightness  = LED_MODE_AUTO,
	},
};

static int as7716_24sc_led_suspend(struct platform_device *dev,
		pm_message_t state)
{
	int i = 0;
	
	for (i = 0; i < ARRAY_SIZE(as7716_24sc_leds); i++) {
		led_classdev_suspend(&as7716_24sc_leds[i]);
	}

	return 0;
}

static int as7716_24sc_led_resume(struct platform_device *dev)
{
	int i = 0;
	
	for (i = 0; i < ARRAY_SIZE(as7716_24sc_leds); i++) {
		led_classdev_resume(&as7716_24sc_leds[i]);
	}

	return 0;
}

static int as7716_24sc_led_probe(struct platform_device *pdev)
{
	int ret, i;

	for (i = 0; i < ARRAY_SIZE(as7716_24sc_leds); i++) {
		ret = led_classdev_register(&pdev->dev, &as7716_24sc_leds[i]);
		
		if (ret < 0)
			break;
	}
	
	/* Check if all LEDs were successfully registered */
	if (i != ARRAY_SIZE(as7716_24sc_leds)){
		int j;
		
		/* only unregister the LEDs that were successfully registered */
		for (j = 0; j < i; j++) {
			led_classdev_unregister(&as7716_24sc_leds[i]);
		}
	}

	return ret;
}

static int as7716_24sc_led_remove(struct platform_device *pdev)
{
	int i;

	for (i = 0; i < ARRAY_SIZE(as7716_24sc_leds); i++) {
		led_classdev_unregister(&as7716_24sc_leds[i]);
	}

	return 0;
}

static struct platform_driver as7716_24sc_led_driver = {
	.probe	 = as7716_24sc_led_probe,
	.remove	 = as7716_24sc_led_remove,
	.suspend = as7716_24sc_led_suspend,
	.resume	 = as7716_24sc_led_resume,
	.driver	 = {
	.name   = DRVNAME,
	.owner  = THIS_MODULE,
	},
};

static int __init as7716_24sc_led_init(void)
{
	int ret;

	ret = platform_driver_register(&as7716_24sc_led_driver);
	if (ret < 0) {
		goto exit;
	}

	ledctl = kzalloc(sizeof(struct as7716_24sc_led_data), GFP_KERNEL);
	if (!ledctl) {
		ret = -ENOMEM;
		platform_driver_unregister(&as7716_24sc_led_driver);
		goto exit;
	}

	mutex_init(&ledctl->update_lock);

	ledctl->pdev = platform_device_register_simple(DRVNAME, -1, NULL, 0);
	if (IS_ERR(ledctl->pdev)) {
		ret = PTR_ERR(ledctl->pdev);
		platform_driver_unregister(&as7716_24sc_led_driver);
		kfree(ledctl);
		goto exit;
	}

exit:
	return ret;
}

static void __exit as7716_24sc_led_exit(void)
{
	platform_device_unregister(ledctl->pdev);
	platform_driver_unregister(&as7716_24sc_led_driver);
	kfree(ledctl);
}

module_init(as7716_24sc_led_init);
module_exit(as7716_24sc_led_exit);

MODULE_AUTHOR("Brandon Chuang <brandon_chuang@accton.com.tw>");
MODULE_DESCRIPTION("as7716_24sc_led driver");
MODULE_LICENSE("GPL");

