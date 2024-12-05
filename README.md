# SerialTest
Because the company needs to frequently test the serial port function, various online serial port management or testing programs either have advertisements or complex functions, making it difficult to use, so I wrote one myself. Multi serial port testing utility.

因为公司要频繁测试串口功能，网上各种串口管理或测试程序不是有广告就是功能复杂，使用麻烦，故自己写了一个。多串口测试实用程序。

COM.UI is the QT interface file, and COM.PY is the QT interface file converted to a PY file. Dragon.ico is an icon used for file printing. You can choose your favorite icon. DragonS2. py is the main code.

COM.UI 为QT界面文件，COM.PY是转换为PY文件的QT界面文件。
dragon.ico 是文件打印用的图标。可以选择自己喜欢的图标。
DragonS2.py是主代码。


--The program idea is very simple. Generally, when we test the serial port, we open the serial port with fixed parameters of 9600, 8, N, and then short-circuit the RX input and TX output. If we can receive the data sent by ourselves through the loop, it is judged as OK.
--Because the company's products have 1 to 4 or even more serial ports, during previous testing, it was very troublesome to set parameters one by one, then open the serial port, send data, short circuit RX TX, and see the received data. Then there was real-time update of the number of serial ports, and a thread was created for each serial port through multithreading to send and receive tests.
--As a tester, you only need to open the tool and short-circuit RX TX one by one to see if the serial port is OK. It is extremely easy to use.

---Of course, there are also drawbacks:
---1. Using QT as the interface, the interface pops up slowly when opened, making it easy for people to misunderstand that it has not been opened.
-----This is because I happened to be learning QT and it was relatively simple. I did it well and didn't want to trouble myself anymore, so I didn't do it. I originally planned to use TKiner for the interface, which should be faster.
---2. The program has poor compatibility with Linux. Under Linux, there may be a lot of virtual tty information that needs to be removed during traversal. In reality, only ttyUSBx is used.
-----There is still a permission issue when accessing serial ports under Linux. Successfully operated FT232RL serial port through Python. Put the user in the dialout group first, which can solve the problem. Sudo usermod - aG dialout f7n (username), serial port name is ttyUSB0 or ttyUSB1

-- 程序想法很简单，一般我们测试串口时都是通过9600，8，N 固定参数打开串口，然后RX输入TX输出短接，能通过回环收到自己发出的数据就判定为OK。
-- 因为公司产品有1到4个，甚至更多串口，之前测试时是一个一个设置参数然后打开串口，发数据，短接RX TX后看收到的数据，非常麻烦。然后就有了实时更新串口数量，通过多线程为每个串口建一个线程来收发测试。
-- 作为使用的测试人员，只需打开工具，然后一个一个串口短接RX TX就能看出串口是否OK。使用起来简单至极。

---当然也有缺点：
---1.用了QT做界面，打开时界面弹出慢，让人容易误解以为没打开。
-----这个因为刚好学习QT，然后比较简单，做好了，又不想再麻烦，没弄。原本想用TKiner来做界面，应该会快些。
---2.程序兼容linux性差。在linux下可能会出很多虚拟的tty信息，在遍历时要把这些都剔除，实际只用ttyUSBx 。
-----linux下访问串口还有个权限问题。通过python操作FT232RL串口成功。 先把用户放到dialout组，可解决。sudo usermod -aG dialout f7n(用户名),串口名是ttyUSB0或ttyUSB1

英文水平不大好，上面英文都是通过百度翻译直接机译的。
