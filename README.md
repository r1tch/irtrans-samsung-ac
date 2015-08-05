# Samsung Air Conditioner Remote Control Codes for IRTrans

This is strongly specific to [IRTrans](http://irtrans.de) IR devices and their
software.

## Initial Setup

Just copy the samsungac.rem file into the remotes/ directory
(`/usr/local/irtrans/remotes/` on my host) and restart irserver.

## Usage

I assume you can use irclient & co.

When naming IR commands, following convention was used:

```
,------- Extra flags; N - no flags, Q - quiet, S - smart saver (yes, they're mutually exclusive)
|,------ Fan speed: Auto, Low, Mid, High
||,----- Swing or Noswing
|||,---- main function: Auto Cool Dry Fan Heat
|||| ,-- temperature, or XX if not applicable (eg fan-only mode)
NASC16
```

Note: there are limitations:
- "off" is an extra command, turns the unit off (surprise!)
- smart saver minimum temperature is 24C
- Auto function: fan speed will also be auto
- Fan function: only fan speed and swing can be set, nothing else
- Test unit does not support setting swing flap angle, only turn swing on/off
- Dry function: min temperature is 18C

## Internals, IR Sequence Structure

### How I Did It

I used IRTrans' learning capability and deduced the rules. The only problem I
came across was replaying the `off` sequence: while having it successfully
learned, IRTrans claimed it was too long for this device to play back.

The learned sequence:

`[off][T]0[D]4301000000010011011111000000000000000000000000000000000011231000000001001011111100000000000000000000000000000000000023100000000100110011110101100011100000000010001000000000110`

I desperately tried to shorten it at the end - to no avail. But at least I
found out I had to remove one single digit to make it digestable for IRTrans.
Then I noticed the many zeros -- I guessed these resemble silence, hence we
could shorten the code here. So removing one single zero made the sequence
work! The working, digestable sequence:

`[off][T]0[D]430100000001001101111100000000000000000000000000000000011231000000001001011111100000000000000000000000000000000000023100000000100110011110101100011100000000010001000000000110`

Conclusion: do not buy IRTrans.....

### .rem Generator

After having the format discovered, it was easy-peasy to create a generator script.

### Sequence Format

```
                                                                                         ,-chksum  ,- noSwing if both bits on
                                                                                         |         |    ,- smart saver, all 3 bits
                                                                                         |         |    |           ,- temp, 0=16C, 14=30C
                                                                                         |         |    |           | ,,,- auto/fan - see below
                                                                                         |         |    |           | |||,- cooling
                               ,- other checksum                                         |        ,|    |           | ||||,-drying
                            cccc                                ,-quiet                  ccccc   / |  sss        vvvv |||||,-heating
  [NASC16][T]1[D]S30100000001001001111100000000000000000000000000000000111123100000000100100011110101100011100000000010001000000011110
```

* The binary values have the bits inverted (LSB comes first, kind-of binary little endian?) This means 001 means 4, 100 means 1.
* Message seems to have two parts, separated by '231' sequence -- each has its own checksum
* Checksum seems to be a constant (18 for first, 32 for 2nd) minus number of bits in remainder of the unit
* The auto/fan bit triplet values can be:
  * 011 - auto function mode
  * 010 - low fan
  * 001 - med fan
  * 000 - auto fan
  * 101 - high fan


## TODO

The remote control can also send:
* auto clean instruction
* timed on/off instructions (ie turn on with these params after 2 hours)

## Raspberry Pi Extra Notes

In short, in the source of irserver, rename the directory `n800` to `arm`.

IRTrans' irserver source is only partly open-source. There's the ccf.o file
that's distributed as an object file, without the source :(

They provide x86, x64 and arm ccf.o files; but they misnamed the arm directory.
I guess they planned to use IRTrans on Nokia n800..???

