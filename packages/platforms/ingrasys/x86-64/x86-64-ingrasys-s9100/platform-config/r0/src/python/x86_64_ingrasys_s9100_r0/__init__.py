from onl.platform.base import *
from onl.platform.ingrasys import *
import os

class OnlPlatform_x86_64_ingrasys_s9100_r0(OnlPlatformIngrasys):
    PLATFORM='x86-64-ingrasys-s9100-r0'
    MODEL="s9100"
    SYS_OBJECT_ID=".8.1"
    
    def baseconfig(self):
                
        os.system("modprobe i2c_ismt")
        self.insmod("eeprom_mb")
        os.system("modprobe w83795")
        os.system("modprobe eeprom")
        os.system("modprobe gpio_pca953x")
        self.insmod("optoe")
        
        ########### initialize I2C bus 1 ###########
        self.new_i2c_device('pca9548', 0x70, 1)
                   
        # initialize i2c
        self.new_i2c_devices(
            [
                ('pca9548', 0x71, 2),
                ('pca9548', 0x72, 3),
                ('pca9548', 0x73, 4),
                ('pca9548', 0x74, 5),
                ]
            )       
    
        # initialize SMBUS0 IO Expander
        os.system("i2cset -y 0 0x27 4 0x00")
        os.system("i2cset -y 0 0x27 5 0x00")
        os.system("i2cset -y 0 0x27 2 0x00")
        os.system("i2cset -y 0 0x27 3 0x00")
        os.system("i2cset -y 0 0x27 6 0xFF")
        os.system("i2cset -y 0 0x27 7 0xFF")
        
        # initialize SMBUS1 ABS
        os.system("i2cset -y 6 0x20 4 0x00")
        os.system("i2cset -y 6 0x20 5 0x00")
        os.system("i2cset -y 6 0x20 6 0xFF")
        os.system("i2cset -y 6 0x20 7 0xFF")

        os.system("i2cset -y 6 0x21 4 0x00")
        os.system("i2cset -y 6 0x21 5 0x00")
        os.system("i2cset -y 6 0x21 6 0xFF")
        os.system("i2cset -y 6 0x21 7 0xFF")
        # initialize Transcevior INT
        os.system("i2cset -y -r 6 0x22 4 0x00")
        os.system("i2cset -y -r 6 0x22 5 0x00")
        os.system("i2cset -y -r 6 0x22 6 0xFF")
        os.system("i2cset -y -r 6 0x22 7 0xFF")

        os.system("i2cset -y -r 6 0x23 4 0x00")
        os.system("i2cset -y -r 6 0x23 5 0x00")
        os.system("i2cset -y -r 6 0x23 6 0xFF")
        os.system("i2cset -y -r 6 0x23 7 0xFF")

         # initialize set ZQSFP LP_MODE = 0 
        os.system("i2cset -y -r 7 0x20 4 0x00")
        os.system("i2cset -y -r 7 0x20 5 0x00")
        os.system("i2cset -y -r 7 0x20 2 0x00")
        os.system("i2cset -y -r 7 0x20 3 0x00")
        os.system("i2cset -y -r 7 0x20 6 0x00")
        os.system("i2cset -y -r 7 0x20 7 0x00")

        os.system("i2cset -y -r 7 0x21 4 0x00")
        os.system("i2cset -y -r 7 0x21 5 0x00")
        os.system("i2cset -y -r 7 0x21 2 0x00")
        os.system("i2cset -y -r 7 0x21 3 0x00")
        os.system("i2cset -y -r 7 0x21 6 0x00")
        os.system("i2cset -y -r 7 0x21 7 0x00")

        # initialize set ZQSFP RST = 1 
        os.system("i2cset -y -r 7 0x22 4 0x00")
        os.system("i2cset -y -r 7 0x22 5 0x00")
        os.system("i2cset -y -r 7 0x22 2 0xFF")
        os.system("i2cset -y -r 7 0x22 3 0xFF")
        os.system("i2cset -y -r 7 0x22 6 0x00")
        os.system("i2cset -y -r 7 0x22 7 0x00")

        os.system("i2cset -y -r 7 0x23 4 0x00")
        os.system("i2cset -y -r 7 0x23 5 0x00")
        os.system("i2cset -y -r 7 0x23 2 0xFF")
        os.system("i2cset -y -r 7 0x23 3 0xFF")
        os.system("i2cset -y -r 7 0x23 6 0x00")
        os.system("i2cset -y -r 7 0x23 7 0x00")

        # initialize set ZQSFP mode 
        os.system("i2cset -y -r 7 0x24 4 0x00")
        os.system("i2cset -y -r 7 0x24 5 0x00")
        os.system("i2cset -y -r 7 0x24 2 0x00")
        os.system("i2cset -y -r 7 0x24 3 0x00")
        os.system("i2cset -y -r 7 0x24 6 0x00")
        os.system("i2cset -y -r 7 0x24 7 0x00")

        os.system("i2cset -y -r 7 0x25 4 0x00")
        os.system("i2cset -y -r 7 0x25 5 0x00")
        os.system("i2cset -y -r 7 0x25 2 0x00")
        os.system("i2cset -y -r 7 0x25 3 0x00")
        os.system("i2cset -y -r 7 0x25 6 0x00")
        os.system("i2cset -y -r 7 0x25 7 0x00")

        # initialize ZQSFP/SFP+/E-Card General 
        os.system("i2cset -y -r 8 0x20 4 0x00")
        os.system("i2cset -y -r 8 0x20 5 0x00")
        os.system("i2cset -y -r 8 0x20 6 0xFF")
        os.system("i2cset -y -r 8 0x20 7 0xFF")
        
        # initialize LED board after PVT (S9100_IO_EXP_LED_ID)
        os.system("i2cset -y -r 9 0x22 4 0x00")
        os.system("i2cset -y -r 9 0x22 5 0x00")
        os.system("i2cset -y -r 9 0x22 6 0x00")
        os.system("i2cset -y -r 9 0x22 7 0x00")

        # initialize PSU I/O (S9100_IO_EXP_PSU_ID)
        os.system("i2cset -y -r 8 0x23 4 0x00")
        os.system("i2cset -y -r 8 0x23 5 0x00")
        os.system("i2cset -y -r 8 0x23 2 0x00")
        os.system("i2cset -y -r 8 0x23 3 0x00")
        os.system("i2cset -y -r 8 0x23 6 0xBB")
        os.system("i2cset -y -r 8 0x23 7 0xFF")
        
        # initialize ABS Port 0-15
        self.new_i2c_device('pca9535', 0x20, 6)
        os.system("echo 496 > /sys/class/gpio/export") 
        os.system("echo 497 > /sys/class/gpio/export") 
        os.system("echo 498 > /sys/class/gpio/export")
        os.system("echo 499 > /sys/class/gpio/export")
        os.system("echo 500 > /sys/class/gpio/export")
        os.system("echo 501 > /sys/class/gpio/export")
        os.system("echo 502 > /sys/class/gpio/export")
        os.system("echo 503 > /sys/class/gpio/export")
        os.system("echo 504 > /sys/class/gpio/export")
        os.system("echo 505 > /sys/class/gpio/export")
        os.system("echo 506 > /sys/class/gpio/export")
        os.system("echo 507 > /sys/class/gpio/export")
        os.system("echo 508 > /sys/class/gpio/export")
        os.system("echo 509 > /sys/class/gpio/export")
        os.system("echo 510 > /sys/class/gpio/export")
        os.system("echo 511 > /sys/class/gpio/export")
        os.system("echo 1 > /sys/class/gpio/gpio496/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio497/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio498/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio499/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio500/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio501/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio502/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio503/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio504/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio505/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio506/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio507/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio508/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio509/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio510/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio511/active_low")
        
        # initialize ABS Port 16-31
        self.new_i2c_device('pca9535', 0x21, 6)
        os.system("echo 480 > /sys/class/gpio/export")
        os.system("echo 481 > /sys/class/gpio/export")
        os.system("echo 482 > /sys/class/gpio/export")
        os.system("echo 483 > /sys/class/gpio/export")
        os.system("echo 484 > /sys/class/gpio/export")
        os.system("echo 485 > /sys/class/gpio/export")
        os.system("echo 486 > /sys/class/gpio/export")
        os.system("echo 487 > /sys/class/gpio/export")
        os.system("echo 488 > /sys/class/gpio/export")
        os.system("echo 489 > /sys/class/gpio/export")
        os.system("echo 490 > /sys/class/gpio/export")
        os.system("echo 491 > /sys/class/gpio/export")
        os.system("echo 492 > /sys/class/gpio/export")
        os.system("echo 493 > /sys/class/gpio/export")
        os.system("echo 494 > /sys/class/gpio/export")
        os.system("echo 495 > /sys/class/gpio/export")
        os.system("echo 1 > /sys/class/gpio/gpio480/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio481/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio482/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio483/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio484/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio485/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio486/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio487/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio488/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio489/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio490/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio491/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio492/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio493/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio494/active_low") 
        os.system("echo 1 > /sys/class/gpio/gpio495/active_low")
        
        # initialize INT Port 0-15
        self.new_i2c_device('pca9535', 0x22, 6)
        os.system("echo 464 > /sys/class/gpio/export")
        os.system("echo 465 > /sys/class/gpio/export")
        os.system("echo 466 > /sys/class/gpio/export")
        os.system("echo 467 > /sys/class/gpio/export")
        os.system("echo 468 > /sys/class/gpio/export")
        os.system("echo 469 > /sys/class/gpio/export")
        os.system("echo 470 > /sys/class/gpio/export")
        os.system("echo 471 > /sys/class/gpio/export")
        os.system("echo 472 > /sys/class/gpio/export")
        os.system("echo 473 > /sys/class/gpio/export")
        os.system("echo 474 > /sys/class/gpio/export")
        os.system("echo 475 > /sys/class/gpio/export")
        os.system("echo 476 > /sys/class/gpio/export")
        os.system("echo 477 > /sys/class/gpio/export")
        os.system("echo 478 > /sys/class/gpio/export")
        os.system("echo 479 > /sys/class/gpio/export")
        os.system("echo 1 > /sys/class/gpio/gpio464/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio465/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio466/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio467/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio468/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio469/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio470/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio471/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio472/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio473/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio474/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio475/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio476/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio477/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio478/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio479/active_low")

        # initialize INT Port 16-31
        self.new_i2c_device('pca9535', 0x23, 6)
        os.system("echo 448 > /sys/class/gpio/export")
        os.system("echo 449 > /sys/class/gpio/export")
        os.system("echo 450 > /sys/class/gpio/export")
        os.system("echo 451 > /sys/class/gpio/export")
        os.system("echo 452 > /sys/class/gpio/export")
        os.system("echo 453 > /sys/class/gpio/export")
        os.system("echo 454 > /sys/class/gpio/export")
        os.system("echo 455 > /sys/class/gpio/export")
        os.system("echo 456 > /sys/class/gpio/export")
        os.system("echo 457 > /sys/class/gpio/export")
        os.system("echo 458 > /sys/class/gpio/export")
        os.system("echo 459 > /sys/class/gpio/export")
        os.system("echo 460 > /sys/class/gpio/export")
        os.system("echo 461 > /sys/class/gpio/export")
        os.system("echo 462 > /sys/class/gpio/export")
        os.system("echo 463 > /sys/class/gpio/export")
        os.system("echo 1 > /sys/class/gpio/gpio448/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio449/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio450/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio451/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio452/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio453/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio454/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio455/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio456/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio457/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio458/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio459/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio460/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio461/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio462/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio463/active_low")
        
        # initialize LP Mode Port 0-15
        self.new_i2c_device('pca9535', 0x20, 7)        
        os.system("echo 432 > /sys/class/gpio/export")
        os.system("echo 433 > /sys/class/gpio/export")
        os.system("echo 434 > /sys/class/gpio/export")
        os.system("echo 435 > /sys/class/gpio/export")
        os.system("echo 436 > /sys/class/gpio/export")
        os.system("echo 437 > /sys/class/gpio/export")
        os.system("echo 438 > /sys/class/gpio/export")
        os.system("echo 439 > /sys/class/gpio/export")
        os.system("echo 440 > /sys/class/gpio/export")
        os.system("echo 441 > /sys/class/gpio/export")
        os.system("echo 442 > /sys/class/gpio/export")
        os.system("echo 443 > /sys/class/gpio/export")
        os.system("echo 444 > /sys/class/gpio/export")
        os.system("echo 445 > /sys/class/gpio/export")
        os.system("echo 446 > /sys/class/gpio/export")
        os.system("echo 447 > /sys/class/gpio/export")
        os.system("echo out > /sys/class/gpio/gpio432/direction")
        os.system("echo out > /sys/class/gpio/gpio433/direction")
        os.system("echo out > /sys/class/gpio/gpio434/direction")
        os.system("echo out > /sys/class/gpio/gpio435/direction")
        os.system("echo out > /sys/class/gpio/gpio436/direction")
        os.system("echo out > /sys/class/gpio/gpio437/direction")
        os.system("echo out > /sys/class/gpio/gpio438/direction")
        os.system("echo out > /sys/class/gpio/gpio439/direction")
        os.system("echo out > /sys/class/gpio/gpio440/direction")
        os.system("echo out > /sys/class/gpio/gpio441/direction")
        os.system("echo out > /sys/class/gpio/gpio442/direction")
        os.system("echo out > /sys/class/gpio/gpio443/direction")
        os.system("echo out > /sys/class/gpio/gpio444/direction")
        os.system("echo out > /sys/class/gpio/gpio445/direction")
        os.system("echo out > /sys/class/gpio/gpio446/direction")
        os.system("echo out > /sys/class/gpio/gpio447/direction")
        
        # initialize LP Mode Port 16-31 
        self.new_i2c_device('pca9535', 0x21, 7)
        os.system("echo 416 > /sys/class/gpio/export")
        os.system("echo 417 > /sys/class/gpio/export")
        os.system("echo 418 > /sys/class/gpio/export")
        os.system("echo 419 > /sys/class/gpio/export")
        os.system("echo 420 > /sys/class/gpio/export")
        os.system("echo 421 > /sys/class/gpio/export")
        os.system("echo 422 > /sys/class/gpio/export")
        os.system("echo 423 > /sys/class/gpio/export")
        os.system("echo 424 > /sys/class/gpio/export")
        os.system("echo 425 > /sys/class/gpio/export")
        os.system("echo 426 > /sys/class/gpio/export")
        os.system("echo 427 > /sys/class/gpio/export")
        os.system("echo 428 > /sys/class/gpio/export")
        os.system("echo 429 > /sys/class/gpio/export")
        os.system("echo 430 > /sys/class/gpio/export")
        os.system("echo 431 > /sys/class/gpio/export")
      
        os.system("echo out > /sys/class/gpio/gpio416/direction")
        os.system("echo out > /sys/class/gpio/gpio417/direction")
        os.system("echo out > /sys/class/gpio/gpio418/direction")
        os.system("echo out > /sys/class/gpio/gpio419/direction")
        os.system("echo out > /sys/class/gpio/gpio420/direction")
        os.system("echo out > /sys/class/gpio/gpio421/direction")
        os.system("echo out > /sys/class/gpio/gpio422/direction")
        os.system("echo out > /sys/class/gpio/gpio423/direction")
        os.system("echo out > /sys/class/gpio/gpio424/direction")
        os.system("echo out > /sys/class/gpio/gpio425/direction")
        os.system("echo out > /sys/class/gpio/gpio426/direction")
        os.system("echo out > /sys/class/gpio/gpio427/direction")
        os.system("echo out > /sys/class/gpio/gpio428/direction")
        os.system("echo out > /sys/class/gpio/gpio429/direction")
        os.system("echo out > /sys/class/gpio/gpio430/direction")
        os.system("echo out > /sys/class/gpio/gpio431/direction")
        
        # initialize RST Port 0-15 
        self.new_i2c_device('pca9535', 0x22, 7)        
        os.system("echo 400 > /sys/class/gpio/export")
        os.system("echo 401 > /sys/class/gpio/export")
        os.system("echo 402 > /sys/class/gpio/export")
        os.system("echo 403 > /sys/class/gpio/export")
        os.system("echo 404 > /sys/class/gpio/export")
        os.system("echo 405 > /sys/class/gpio/export")
        os.system("echo 406 > /sys/class/gpio/export")
        os.system("echo 407 > /sys/class/gpio/export")
        os.system("echo 408 > /sys/class/gpio/export")
        os.system("echo 409 > /sys/class/gpio/export")
        os.system("echo 410 > /sys/class/gpio/export")
        os.system("echo 411 > /sys/class/gpio/export")
        os.system("echo 412 > /sys/class/gpio/export")
        os.system("echo 413 > /sys/class/gpio/export")
        os.system("echo 414 > /sys/class/gpio/export")
        os.system("echo 415 > /sys/class/gpio/export")
        os.system("echo out > /sys/class/gpio/gpio400/direction")
        os.system("echo out > /sys/class/gpio/gpio401/direction")
        os.system("echo out > /sys/class/gpio/gpio402/direction")
        os.system("echo out > /sys/class/gpio/gpio403/direction")
        os.system("echo out > /sys/class/gpio/gpio404/direction")
        os.system("echo out > /sys/class/gpio/gpio405/direction")
        os.system("echo out > /sys/class/gpio/gpio406/direction")
        os.system("echo out > /sys/class/gpio/gpio407/direction")
        os.system("echo out > /sys/class/gpio/gpio408/direction")
        os.system("echo out > /sys/class/gpio/gpio409/direction")
        os.system("echo out > /sys/class/gpio/gpio410/direction")
        os.system("echo out > /sys/class/gpio/gpio411/direction")
        os.system("echo out > /sys/class/gpio/gpio412/direction")
        os.system("echo out > /sys/class/gpio/gpio413/direction")
        os.system("echo out > /sys/class/gpio/gpio414/direction")
        os.system("echo out > /sys/class/gpio/gpio415/direction")
        os.system("echo 1 > /sys/class/gpio/gpio400/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio401/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio402/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio403/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio404/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio405/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio406/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio407/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio408/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio409/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio410/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio411/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio412/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio413/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio414/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio415/active_low")
        os.system("echo 0 > /sys/class/gpio/gpio400/value")
        os.system("echo 0 > /sys/class/gpio/gpio401/value")
        os.system("echo 0 > /sys/class/gpio/gpio402/value")
        os.system("echo 0 > /sys/class/gpio/gpio403/value")
        os.system("echo 0 > /sys/class/gpio/gpio404/value")
        os.system("echo 0 > /sys/class/gpio/gpio405/value")
        os.system("echo 0 > /sys/class/gpio/gpio406/value")
        os.system("echo 0 > /sys/class/gpio/gpio407/value")
        os.system("echo 0 > /sys/class/gpio/gpio408/value")
        os.system("echo 0 > /sys/class/gpio/gpio409/value")
        os.system("echo 0 > /sys/class/gpio/gpio410/value")
        os.system("echo 0 > /sys/class/gpio/gpio411/value")
        os.system("echo 0 > /sys/class/gpio/gpio412/value")
        os.system("echo 0 > /sys/class/gpio/gpio413/value")
        os.system("echo 0 > /sys/class/gpio/gpio414/value")
        os.system("echo 0 > /sys/class/gpio/gpio415/value")
        
        # initialize RST Port 16-31
        self.new_i2c_device('pca9535', 0x23, 7)
        os.system("echo 384 > /sys/class/gpio/export")
        os.system("echo 385 > /sys/class/gpio/export")
        os.system("echo 386 > /sys/class/gpio/export")
        os.system("echo 387 > /sys/class/gpio/export")
        os.system("echo 388 > /sys/class/gpio/export")
        os.system("echo 389 > /sys/class/gpio/export")
        os.system("echo 390 > /sys/class/gpio/export")
        os.system("echo 391 > /sys/class/gpio/export")
        os.system("echo 392 > /sys/class/gpio/export")
        os.system("echo 393 > /sys/class/gpio/export")
        os.system("echo 394 > /sys/class/gpio/export")
        os.system("echo 395 > /sys/class/gpio/export")
        os.system("echo 396 > /sys/class/gpio/export")
        os.system("echo 397 > /sys/class/gpio/export")
        os.system("echo 398 > /sys/class/gpio/export")
        os.system("echo 399 > /sys/class/gpio/export")
        os.system("echo out > /sys/class/gpio/gpio384/direction")
        os.system("echo out > /sys/class/gpio/gpio385/direction")
        os.system("echo out > /sys/class/gpio/gpio386/direction")
        os.system("echo out > /sys/class/gpio/gpio387/direction")
        os.system("echo out > /sys/class/gpio/gpio388/direction")
        os.system("echo out > /sys/class/gpio/gpio389/direction")
        os.system("echo out > /sys/class/gpio/gpio390/direction")
        os.system("echo out > /sys/class/gpio/gpio391/direction")
        os.system("echo out > /sys/class/gpio/gpio392/direction")
        os.system("echo out > /sys/class/gpio/gpio393/direction")
        os.system("echo out > /sys/class/gpio/gpio394/direction")
        os.system("echo out > /sys/class/gpio/gpio395/direction")
        os.system("echo out > /sys/class/gpio/gpio396/direction")
        os.system("echo out > /sys/class/gpio/gpio397/direction")
        os.system("echo out > /sys/class/gpio/gpio398/direction")
        os.system("echo out > /sys/class/gpio/gpio399/direction")
        os.system("echo 1 > /sys/class/gpio/gpio384/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio385/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio386/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio387/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio388/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio389/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio390/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio391/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio392/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio393/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio394/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio395/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio396/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio397/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio398/active_low")
        os.system("echo 1 > /sys/class/gpio/gpio399/active_low")
        os.system("echo 0 > /sys/class/gpio/gpio384/value")
        os.system("echo 0 > /sys/class/gpio/gpio385/value")
        os.system("echo 0 > /sys/class/gpio/gpio386/value")
        os.system("echo 0 > /sys/class/gpio/gpio387/value")
        os.system("echo 0 > /sys/class/gpio/gpio388/value")
        os.system("echo 0 > /sys/class/gpio/gpio389/value")
        os.system("echo 0 > /sys/class/gpio/gpio390/value")
        os.system("echo 0 > /sys/class/gpio/gpio391/value")
        os.system("echo 0 > /sys/class/gpio/gpio392/value")
        os.system("echo 0 > /sys/class/gpio/gpio393/value")
        os.system("echo 0 > /sys/class/gpio/gpio394/value")
        os.system("echo 0 > /sys/class/gpio/gpio395/value")
        os.system("echo 0 > /sys/class/gpio/gpio396/value")
        os.system("echo 0 > /sys/class/gpio/gpio397/value")
        os.system("echo 0 > /sys/class/gpio/gpio398/value")
        os.system("echo 0 > /sys/class/gpio/gpio399/value")
        
        # initialize MODSEL Port 0-15
        self.new_i2c_device('pca9535', 0x24, 7)
        os.system("echo 368 > /sys/class/gpio/export")
        os.system("echo 369 > /sys/class/gpio/export")
        os.system("echo 370 > /sys/class/gpio/export")
        os.system("echo 371 > /sys/class/gpio/export")
        os.system("echo 372 > /sys/class/gpio/export")
        os.system("echo 373 > /sys/class/gpio/export")
        os.system("echo 374 > /sys/class/gpio/export")
        os.system("echo 375 > /sys/class/gpio/export")
        os.system("echo 376 > /sys/class/gpio/export")
        os.system("echo 377 > /sys/class/gpio/export")
        os.system("echo 378 > /sys/class/gpio/export")
        os.system("echo 379 > /sys/class/gpio/export")
        os.system("echo 380 > /sys/class/gpio/export")
        os.system("echo 381 > /sys/class/gpio/export")
        os.system("echo 382 > /sys/class/gpio/export")
        os.system("echo 383 > /sys/class/gpio/export")
        os.system("echo out > /sys/class/gpio/gpio368/direction")
        os.system("echo out > /sys/class/gpio/gpio369/direction")
        os.system("echo out > /sys/class/gpio/gpio370/direction")
        os.system("echo out > /sys/class/gpio/gpio371/direction")
        os.system("echo out > /sys/class/gpio/gpio372/direction")
        os.system("echo out > /sys/class/gpio/gpio373/direction")
        os.system("echo out > /sys/class/gpio/gpio374/direction")
        os.system("echo out > /sys/class/gpio/gpio375/direction")
        os.system("echo out > /sys/class/gpio/gpio376/direction")
        os.system("echo out > /sys/class/gpio/gpio377/direction")
        os.system("echo out > /sys/class/gpio/gpio378/direction")
        os.system("echo out > /sys/class/gpio/gpio379/direction")
        os.system("echo out > /sys/class/gpio/gpio380/direction")
        os.system("echo out > /sys/class/gpio/gpio381/direction")
        os.system("echo out > /sys/class/gpio/gpio382/direction")
        os.system("echo out > /sys/class/gpio/gpio383/direction")
        
        # initialize MODSEL Port 16-31
        self.new_i2c_device('pca9535', 0x25, 7)        
        os.system("echo 352 > /sys/class/gpio/export")
        os.system("echo 353> /sys/class/gpio/export")
        os.system("echo 354> /sys/class/gpio/export")
        os.system("echo 355> /sys/class/gpio/export")
        os.system("echo 356 > /sys/class/gpio/export")
        os.system("echo 357 > /sys/class/gpio/export")
        os.system("echo 358 > /sys/class/gpio/export")
        os.system("echo 359 > /sys/class/gpio/export")
        os.system("echo 360 > /sys/class/gpio/export")
        os.system("echo 361 > /sys/class/gpio/export")
        os.system("echo 362 > /sys/class/gpio/export")
        os.system("echo 363 > /sys/class/gpio/export")
        os.system("echo 364 > /sys/class/gpio/export")
        os.system("echo 365 > /sys/class/gpio/export")
        os.system("echo 366 > /sys/class/gpio/export")
        os.system("echo 367 > /sys/class/gpio/export")
        os.system("echo out > /sys/class/gpio/gpio352/direction")
        os.system("echo out > /sys/class/gpio/gpio353/direction")
        os.system("echo out > /sys/class/gpio/gpio354/direction")
        os.system("echo out > /sys/class/gpio/gpio355/direction")
        os.system("echo out > /sys/class/gpio/gpio356/direction")
        os.system("echo out > /sys/class/gpio/gpio357/direction")
        os.system("echo out > /sys/class/gpio/gpio358/direction")
        os.system("echo out > /sys/class/gpio/gpio359/direction")
        os.system("echo out > /sys/class/gpio/gpio360/direction")
        os.system("echo out > /sys/class/gpio/gpio361/direction")
        os.system("echo out > /sys/class/gpio/gpio362/direction")
        os.system("echo out > /sys/class/gpio/gpio363/direction")
        os.system("echo out > /sys/class/gpio/gpio364/direction")
        os.system("echo out > /sys/class/gpio/gpio365/direction")
        os.system("echo out > /sys/class/gpio/gpio366/direction")
        os.system("echo out > /sys/class/gpio/gpio367/direction")
        
        # initialize qsfp eeprom 
        for port in range(1, 33):
            self.new_i2c_device('sff8436', 0x50, port + 9)

        # initialize sys eeprom devices
        self.new_i2c_device('mb_eeprom', 0x54, 9)
        
        # initialize temperature sensor
        os.system("i2cset -y -r -f 0 0x2F 0x00 0x80")
        os.system("i2cset -y -r -f 0 0x2F 0x05 0x7F")
        os.system("i2cset -y -r -f 0 0x2F 0x04 0x0A")  
        
        # initialize psu eeprom devices
        self.new_i2c_device('eeprom', 0x50, 8)
        self.new_i2c_device('eeprom', 0x50, 9)

        # initialize sys led
        os.system("i2cset -m 0x40 -y -r 9 0x22 2 0xFF")
        os.system("i2cset -m 0x80 -y -r 9 0x22 2 0x00")

        # init CPLD LED_CLR Register (Switch Port LED)
        os.system("i2cset -y 0 0x33 0x34 0x10")
        
        # init Fan I/O Exanpler
        os.system("i2cset -y -r 9 0x20 4 0x00")
        os.system("i2cset -y -r 9 0x20 5 0x00")
        os.system("i2cset -y -r 9 0x20 2 0x00")
        os.system("i2cset -y -r 9 0x20 3 0x00")
        os.system("i2cset -y -r 9 0x20 6 0xCC")
        os.system("i2cset -y -r 9 0x20 7 0xCC")

        return True
        
        
