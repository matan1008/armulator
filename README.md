# Description

A pure python ARM emulator

# Installation

Install the last released version using `pip`:

```shell
python3 -m pip install --user -U armulator
```


Or install the latest version from sources:

```shell
git clone git@github.com:matan1008/armulator.git
cd pyiosbackup
python3 -m pip install --user -U -e .
```

# Usage

To create a processor object, you need to import it first:
```python
from armulator.armv6.arm_v6 import ArmV6
```

Then you can just create it:

```python
arm = ArmV6()
```
Getting familiar with the Memory controller concept is crucial for using the processor.  
In short, there is one "hub" to which you can connect several controllers.  
A "Memory Controller" can be a stick of RAM, Memory mapped LCD screen or whatever you wish.  
  
For example, let's create a RAM controller:

```python
from armulator.armv6.memory_types import RAM
from armulator.armv6.memory_controller_hub import MemoryController

mem = RAM(0x100)
mc = MemoryController(mem, 0xF0000000, 0xF0000100)
arm.mem.memories.append(mc)
```

Now, trying to access a memory between 0xF0000000 and 0xF0000100, will access the `mem` object.  
You can also change the memory manually:

```python
mem.write(0, 2, "\xfe\xe7")
```

Another useful feature is playing with the memory protection or management unit,
for example cancelling memory protection will look like:
```python
arm.registers.sctlr.m = 0
arm.take_reset()
```
Please note that after changing internal features it is recommended to reset the processor.  
  
When running the armulator, you will probably want to start from a defined address, so:
```python

arm.registers.branch_to(0x100)
```

The last thing we need to do is to really run the processor, which can be done with:
```python
arm.emulate_cycle()
```


# Running the tests

Running the tests can be done easily with pytest:

```shell
python3 -m pytest tests -vv
```

# Acknowledgments

* At first, I did it to learn the ARM architecture better. I guess I was carried away.
* Feel free to report bugs.
* Feel free to ask for more features.
