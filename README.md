# Armulator

A pure python ARM emulator

## Getting Started

### Prerequisites

The only package required is `bitstring`.
In order to run the tests, `pytest` is required.

```
pip install bitstring
pip install pytest
```

### Installing

Installing the `armulator` is pretty simple. All you need to do is:

```
pip install armulator
```

### Usage

To create a processor object, you need to import it first:
```python
from armulator.armv6.arm_v6 import ArmV6
```

Then you can just create it:

```python
arm = ArmV6()
```
In order to really use the processor it is crutcial to came familiar with the Memory controller concept.  
The main idea of this concept is that there is one "hub" to which you can connect several controllers.  
A "Memory Controller" can be a stick of RAM, Memory mapped LCD screen or whatever you wish.  
  
For example, let's create a RAM controller:

```python
from armulator.armv6.memory_types import RAM
from armulator.armv6.memory_controller_hub import MemoryController
mem = RAM(0x100)
mc = MemoryController(mem, 0xF0000000, 0xF0000100)
arm.mem.memories.append(mc)
```

Now, any try to access a memory between 0xF0000000 and 0xF0000100, will access the `mem` object.  
You can also change the memory manually:

```python
mem.write(0, 2, "\xfe\xe7")
```

Another useful feature is playing with the memory protection or management unit,
for example cancelling memory protection will look like:
```python
arm.registers.sctlr.set_m(False)
arm.take_reset()
```
Please note that after changing internal features it is recommended to reset the processor.  
  
When running the armulator, you will probably want to start from a defined address, so:
```python
from bitstring import BitArray
arm.registers.branch_to(BitArray(uint=0x100, length=32))
```

The last thing we need to do is to really run the processor, which can be done with:
```python
arm.emulate_cycle()
```


## Running the tests

Running the tests can be done easily with pytest:

```python
python -m pytest tests -vv
```

More tests will be added soon.

## Built With

* [bitstring](http://scott-griffiths.github.io/bitstring/) - Used for bits operations

## Authors

* **Matan Perelman** - [matan1008](https://github.com/matan1008)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* At first, I did it to learn the ARM architecture better. I guess I was carried away.
* Feel free to report bugs.
* Feel free to ask for more features.
