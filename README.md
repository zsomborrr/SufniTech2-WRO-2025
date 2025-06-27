
# SufniTech2-WRO-2025

Welcome to the official repository of **SufniTech2-WRO-2025** for the **World Robot Olympiad 2025**.

# About us

We are a beginner robotics team from **Nyíregyháza, Hungary**, we decided to enter the competition due to our mentor's advice though we’ve little experience. Our team consists of:

- **Czirják Róbert** – The newest addition to our team, responsible for building and assembling the robot.
- **Rékási László** – Hardware specialist and key contributor to the robot’s physical development.
- **Angel Zsombor** – Software engineer in charge of writing the code and maintaining our GitHub repository.

# Design

    Hardware

For the build of the robot our team used fischertechnik's [Maker Kit Car](https://www.fischertechnik.de/de-de/maker#maker-kit-car). Then we had 2 additional parts 3D printed onto it included in our models folder. The controller/computer of our choice is the [Raspberry Pi 4 Model B](https://www.fischertechnik.de/de-de/maker#maker-kit-car). We also use the HC-SR04P distance measurement module because it is widely popular and reliable. For color measuring other than the camera which is less reliable there is also a TCS3200 color sensor on the bottom. Obviously as I mentioned there is also a camera for measurement if color but in a different way. The L298N was our choice for the motor controller since we had this on hand. We can't have a motor controller without a motor which we got from the kit along with the servo. The power source of our robot comes from 3 cells.

    Software
   The code uses the python RPi.GPIO library to communicate with the Raspberry. It was edited with a VSCodium SSH client extension and controlled via SSH from terminal.

# Hardships

During development we had faced many challenges and also could not fully finish every function of the robot to it's full extent but that will not stop us from having a good time! :)
